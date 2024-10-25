from sqlmodel import Session, select
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_cookie import EncryptedCookieManager
from models import User


class StreamlitAuth:
    def __init__(self, engine):
        self.engine = engine

        self.cookies = EncryptedCookieManager(
            prefix="streamlit_auth_cookies",
            password='9d68d6f2-4258-45c9-96eb-2d6bc74ddbb5-d8f49cab-edbb-404a-94d0-b25b1d4a564b')
        if not self.cookies.ready():
            st.stop()

        if "user" not in st.session_state:
            if "username" in self.cookies.keys() and str(self.cookies['username']):
                st.session_state.user = self.user = self.get_user(self.cookies['username'])
            else:
                st.session_state.user = self.user = None
        else:
            self.user = st.session_state.user

    def signup(self):
        with st.form("signup_form", border=True):
            st.header("Signup")
            name = st.text_input("Name")
            email = st.text_input("Email")
            username = st.text_input("Username")
            password = st.text_input("Password")
            if st.form_submit_button("Signup", type='primary'):
                with Session(self.engine, expire_on_commit=False) as session:
                    statement = select(User).where(User.username == username or User.email == email)
                    st.session_state.user = session.exec(statement).first()
                if st.session_state.user is None:
                    new_user = User(name=name, email=email, username=username, password=password)
                    with Session(self.engine, expire_on_commit=False) as session:
                        session.add(new_user)
                        session.commit()
                    st.success("User registered successfully", icon="✅")
                else:
                    st.error("The username or email is already exist", icon="❌")

    def signout(self):
        if st.button("Signout"):
            self.user = None
            del st.session_state["user"]
            self.cookies['username'] = ""
            self.cookies.save()
            st.success("Bye", icon="✅")
            st.rerun()

    def signin(self):
        with st.form("signin_form", border=True):
            st.header("Signin")
            username = st.text_input("Username")
            password = st.text_input("Password")
            if st.form_submit_button("Signin", type='primary'):
                with Session(self.engine, expire_on_commit=False) as session:
                    statement = select(User).where(User.username == username and User.password == password)
                    self.user = session.exec(statement).first()
                if self.user:
                    st.session_state.user = self.user
                    self.cookies['username'] = st.session_state.user.username
                    self.cookies.save()
                    st.success("Welcome", icon="✅")
                    st.rerun()
                else:
                    st.error("The username or password is incorrect", icon="❌")

    def get_user(self, username):
        with Session(self.engine, expire_on_commit=False) as session:
            statement = select(User).where(User.username == username)
            return session.exec(statement).first()

    def signup_and_signin(self):
        with st.sidebar:
            selected = option_menu("ChatBot", ["Signin", 'Signup'],
                icons=['house', 'gear'], menu_icon="cast", default_index=0)

        if selected == "Signin":
            self.signin()

        elif selected == "Signup":
            self.signup()
