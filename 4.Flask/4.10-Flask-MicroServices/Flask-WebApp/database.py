import os
from datetime import datetime
from dotenv import load_dotenv
from sqlmodel import Field, SQLModel, create_engine, Session, select


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str
    join_time: str


class Comment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    user_id: int = Field(foreign_key="user.id")


class Topic(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    body: str
    image: str
    timestamp: datetime = Field(default_factory=datetime.now)
    user_id: int = Field(foreign_key="user.id")


# DATABASE_URL = 'sqlite:///./database.db'
# DATABASE_URL = "postgresql://akbar_agha:ramze_akbar_agha@some-postgres:5432/database_akbar_agha"

load_dotenv()

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_URL = (
    f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
)

engine = create_engine(DATABASE_URL, echo=True)

# Create the database tables
SQLModel.metadata.create_all(engine)


def get_user_by_username(username: str):
    with Session(engine) as db_session:
        statement = select(User).where(User.username == username)
        return db_session.exec(statement).first()


def create_user(username: str, password_hash: str):
    user = User(username=username, password=password_hash, join_time=datetime.now())
    with Session(engine) as db_session:
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user
