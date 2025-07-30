from pydantic import BaseModel
from .db_model import WordEntry


class WordStatusInput(BaseModel):
    word: str
    status: int


class NewVocabularyInput(BaseModel):
    word: str
    meaning: str
