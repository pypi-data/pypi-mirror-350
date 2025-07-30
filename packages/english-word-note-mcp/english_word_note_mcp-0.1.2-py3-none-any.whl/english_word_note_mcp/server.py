import json
import os
import random
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List, Union

import aiofiles
from mcp.server import FastMCP
from pydantic import (
    Field as PydanticField,
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select, insert
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import WordEntry, WordStatusInput

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///english_notes.db")
engine = create_async_engine(DATABASE_URL, echo=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def get_data_directory_path():
    return os.getenv("ENGLISH_WORD_NOTE_PATH", "data")


def get_source_english_words_json_path():
    return os.path.join(os.path.dirname(__file__), "data", "english_words.base.json")


@asynccontextmanager
async def lifespan(app: FastMCP):
    await create_db_and_tables()

    yield


server = FastMCP(name="english-word-note-mcp", lifespan=lifespan)


@server.tool()
async def get_english_words(
    num: int = PydanticField(default=20, ge=20, le=100),
):
    """从数据库中随机获取英语单词，排除那些已完全掌握的单词（状态为3）。

    参数:
        num (int): 要获取的单词数量（默认值：20，最小值：20，最大值：100）。

    返回:
        Union[List[str], dict]: 单词列表或错误字典。
    """
    target_words_path = get_source_english_words_json_path()
    words = []

    async with aiofiles.open(target_words_path, "r", encoding="utf-8") as f:
        data = await f.read()

    words = json.loads(data)

    async with AsyncSession(engine) as session:
        statement = select(WordEntry).where(WordEntry.status < 3)
        results = await session.exec(statement)
        available_words = results.all()
        not_remember_words = list(filter(lambda w: w.status == 1, available_words))
        remember_words = list(filter(lambda w: w.status == 2, available_words))

        in_words = [w.word for w in available_words]

        words = [w["word"] for w in words if w not in in_words]

        select_1 = random.sample(not_remember_words, min(num, len(not_remember_words)))
        select_2 = random.sample(remember_words, min(num, len(remember_words)))

        selected_word_entries = select_1 + select_2

        return [word.word for word in selected_word_entries] + list(
            random.sample(words, min(num - len(selected_word_entries), len(words)))
        )


@server.tool()
async def set_word_status(
    word: str = PydanticField(..., description="英语单词"),
    status: int = PydanticField(
        ...,
        description="掌握状态：1（未掌握），2（基本掌握），或3（完全掌握）",
    ),
) -> Union[WordEntry, dict]:
    """在数据库中添加新单词或更新现有单词的状态。

    参数:
        word (str): 英语单词（不区分大小写）。
        status (int): 掌握状态（1：未掌握，2：基本掌握，3：完全掌握）。

    返回:
        Union[WordEntry, dict]: 创建/更新的WordEntry对象或错误字典。
    """
    if status not in [1, 2, 3]:
        return {"error": "状态必须为1（未掌握），2（基本掌握），或3（完全掌握）"}

    async with AsyncSession(engine) as session:
        word_lower = word.lower()
        statement = select(WordEntry).where(WordEntry.word == word_lower)
        results = await session.exec(statement)
        db_entry = results.one_or_none()

        if db_entry:
            db_entry.status = status
            db_entry.last_updated = datetime.now(timezone.utc)
        else:
            db_entry = WordEntry(word=word_lower, status=status)

        session.add(db_entry)
        await session.commit()
        await session.refresh(db_entry)
        return db_entry


@server.tool()
async def insert_words_to_db(
    word_statuses: List[WordStatusInput] = PydanticField(
        ..., description="带有新状态的单词列表"
    ),
):
    """将一批单词及其状态插入到数据库中。

    参数:
        word_statuses: 包含单词和状态的列表。每个元素是一个包含 word 和 status 的字典。
        example:
        [
            {"word": "hello", "status": 1},
            {"word": "world", "status": 2},
        ]

    返回:
        Dict[str, Any]: 操作结果消息。
    """
    if not word_statuses:
        return {"message": "没有要处理的单词。"}

    added_count = 0
    updated_count = 0

    async with AsyncSession(engine) as session:
        valid_words = []
        word_to_status = {}

        for w in word_statuses:
            word_lower = w.word.lower().strip()
            if not word_lower:
                continue
            valid_words.append(word_lower)
            word_to_status[word_lower] = w.status

        if not valid_words:
            return {"message": "没有有效的单词需要处理。"}

        statement = select(WordEntry).where(WordEntry.word.in_(valid_words))  # type: ignore
        results = await session.exec(statement)
        existing_entries = {entry.word: entry for entry in results.all()}

        current_time = datetime.now(timezone.utc)
        for word, entry in existing_entries.items():
            entry.status = word_to_status[word]
            entry.last_updated = current_time
            updated_count += 1

        new_words = set(valid_words) - set(existing_entries.keys())
        if new_words:
            new_entries_data = [
                {
                    "word": word,
                    "status": word_to_status[word],
                    "last_updated": current_time,
                }
                for word in new_words
            ]

            try:
                await session.exec(insert(WordEntry).values(new_entries_data))  # pyright:ignore
                added_count = len(new_entries_data)
            except Exception as e:
                print(f"批量插入失败，错误：{str(e)}。回退到session.add_all()。")
                return {
                    "message": "批量插入失败。",
                    "error": str(e),
                }

        await session.commit()

    return {
        "message": "批量单词状态更新已完成。",
        "added_count": added_count,
        "updated_count": updated_count,
    }


@server.tool()
async def get_word_details(
    word: str = PydanticField(..., description="要获取详细信息的英语单词"),
) -> Union[WordEntry, dict]:
    """获取特定英语单词的记忆情况。

    参数:
        word (str): 英语单词（不区分大小写）。

    返回:
        dict: 单词记忆状态。
    """
    async with AsyncSession(engine) as session:
        statement = select(WordEntry).where(WordEntry.word == word.lower())
        results = await session.exec(statement)
        db_entry = results.one_or_none()

        if db_entry:
            if db_entry.status == 1:
                status_str = "未掌握"
            elif db_entry.status == 2:
                status_str = "基本掌握"
            elif db_entry.status == 3:
                status_str = "完全掌握"
            else:
                status_str = "未知状态"
            return {"msg": f"之前遇到过这个单词，{status_str}"}
        else:
            return {"msg": f"单词 '{word}' 之前未遇到过"}
