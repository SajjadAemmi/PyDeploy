import json
import requests
import datetime
from sqlmodel import Session, SQLModel, create_engine, select
import streamlit as st
from models import Message
from auth import StreamlitAuth


st.set_page_config(
    page_title="ChatBot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="auto")


@st.cache_resource
def connect_to_database():
    engine = create_engine("sqlite:///database.db")
    SQLModel.metadata.create_all(engine)
    return engine


def ai(user_message_text):
    print(user_message_text)
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzgyZDI1ZmEtYWRiOC00ZTcwLWI4OGEtYjUyZDI2NTEyOTY4IiwidHlwZSI6ImFwaV90b2tlbiJ9.OIwcKNh9tV6GVvNOWP7l_BFVnao8_KVPo7kTQdwY8sc"}
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": "Hello i need your help ! ",
        "chatbot_global_action": "Act as an assistant",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 150,
        "fallback_providers": "openai"
    }
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    ai_message_text = result['openai']['generated_text']
    return ai_message_text


def process(user_message_text):
    ai_message_text = ai(user_message_text)

    # backend
    user_message = Message(
        text=user_message_text, 
        time=str(datetime.datetime.now()),
        user_id=auth.user.id,
        type="user")
    ai_message = Message(
        text=ai_message_text, 
        time=str(datetime.datetime.now()),
        user_id=auth.user.id,
        type="ai")
    with Session(engine, expire_on_commit=False) as session:
        session.add(user_message)
        session.add(ai_message)
        session.commit()

    # frontend
    st.session_state.messages.append(user_message)
    st.session_state.messages.append(ai_message)
    return ai_message_text


engine = connect_to_database()
auth = StreamlitAuth(engine)

if auth.user:
    with st.sidebar:
        st.title("My Chatbot")
        st.write(f'Welcome *{st.session_state.user.name}*')
        auth.signout()

    if 'messages' not in st.session_state:
        with Session(engine) as session:
            statement = select(Message).where(Message.user_id == auth.user.id)
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

else:
    auth.signup_and_signin()
