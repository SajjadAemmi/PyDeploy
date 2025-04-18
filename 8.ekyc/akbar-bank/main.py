import requests
import json
import streamlit as st


if "token" in st.session_state:
    st.write("خوش آمدی :)")

    url = "http://127.0.0.1:8000/get-user"
    payload = {}
    headers = {
    'Authorization': 'Bearer ' + st.session_state.token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    level = json.loads(response.text)["level"]

    st.write(f"سطح کاربری شما: {level}")
    col1, col2 = st.columns(2)

    with col1:
        st.info("وضعیت شناسایی چهره")
        st.info("وضعیت شناسایی صدا")
        st.info("وضعیت شناسایی حالت دست")
    with col2:
        st.warning("انجام نشده")
        st.warning("انجام نشده")
        if ...:
            st.success("انجام شده")
        elif ...:
            st.warning("در حال پردازش")
        else:
            st.warning("انجام نشده")

else:
    with st.form("login-form"):
        email = st.text_input("Email")
        password = st.text_input("Password")
        first_name = st.text_input("first_name")
        last_name = st.text_input("last_name")

        if st.form_submit_button('ورود'):
            url = "http://127.0.0.1:8000/signin"

            payload = json.dumps({
            "email": email,
            "password": password
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            st.session_state.token = json.loads(response.text)["access_token"]
