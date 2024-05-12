from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    username: str
    password: str

    messages: list["Message"] = Relationship(back_populates="user")


class Message(SQLModel, table=True):
    __tablename__ = "messages"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    time: str
    type: str
    user_id: int | None = Field(default=None, foreign_key="users.id")

    user: User | None = Relationship(back_populates="messages")
