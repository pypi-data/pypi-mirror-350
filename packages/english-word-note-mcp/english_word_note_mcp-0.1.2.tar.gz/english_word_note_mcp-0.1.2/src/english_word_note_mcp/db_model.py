from sqlmodel import Field, SQLModel
from typing import Optional
import uuid
from datetime import datetime, timezone


class WordEntry(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    word: str = Field(unique=True, index=True, description="The English word.")
    status: int = Field(
        default=1,
        index=True,
        description="Mastery status: 1 (Not Mastered), 2 (Basically Mastered), 3 (Fully Mastered)",
    )
    last_updated: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp of the last update to this word entry.",
    )
