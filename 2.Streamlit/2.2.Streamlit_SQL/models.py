from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship


class Hero(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str

    messages: list["Message"] = Relationship(back_populates="hero")


class Message(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    time: str
    type: str

    hero_id: int | None = Field(default=None, foreign_key="hero.id")
    hero: Hero | None = Relationship(back_populates="messages")
