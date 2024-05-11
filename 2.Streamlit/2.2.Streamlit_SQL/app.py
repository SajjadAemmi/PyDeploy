import datetime
import streamlit as st
from sqlmodel import Field, Session, SQLModel, create_engine, select
from models import Hero, Message


st.set_page_config(
    page_title="پتروپالایش",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Photography AI!"
    }
)


@st.cache_resource
def connect_to_database():
    engine = create_engine("sqlite:///database.db")
    SQLModel.metadata.create_all(engine)
    return engine


@st.cache_resource
def get_hero():
    with Session(engine) as session:
        my_name = "spiderman"
        statement = select(Hero).where(Hero.name == my_name)
        hero = session.exec(statement).first()
        return hero
    

engine = connect_to_database()
hero = get_hero()


def ai(user_message_text):
    return "Hi"


def process(user_message_text):
    ai_message_text = ai(user_message_text)

    # backend
    user_message = Message(text=user_message_text, time=str(datetime.datetime.now()), hero_id=hero.id, type="user")
    ai_message = Message(text=ai_message_text, time=str(datetime.datetime.now()), hero_id=hero.id, type="ai")
    with Session(engine, expire_on_commit=False) as session:
        session.add(user_message)
        session.add(ai_message)
        session.commit()

    # frontend
    st.session_state.messages.append(user_message)
    st.session_state.messages.append(ai_message)
    return ai_message_text

with st.sidebar:
    st.title("My Chatbot")


if 'messages' not in st.session_state:
    with Session(engine) as session:
        statement = select(Message).where(Message.hero_id == hero.id)
        st.session_state.messages = session.exec(statement).all()

for message in st.session_state.messages:
    with st.chat_message(message.type):
        st.markdown(message.text)

if user_message_text := st.chat_input("What is up?"):
        ai_message_text = process(user_message_text)

        with st.chat_message("user"):
            st.markdown(user_message_text)
        with st.chat_message("ai"):
            st.markdown(ai_message_text)
