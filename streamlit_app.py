import uuid

import requests

import streamlit as st


BACKEND_URL = (
    "http://localhost:8000/chat"
)

st.set_page_config(
    page_title="SmartDesk AI"
)

st.title(
    "SmartDesk AI"
)

if "session_id" not in st.session_state:

    st.session_state.session_id = (
        str(uuid.uuid4())
    )

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


user_input = st.chat_input(
    "Ask IT or HR a question..."
)


if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message(
        "user"
    ):
        st.write(user_input)

    payload = {

        "session_id":
        st.session_state.session_id,

        "query":
        user_input
    }

    response = requests.post(
        BACKEND_URL,
        json=payload
    )

    reply = response.json()[
        "response"
    ]

    st.session_state.messages.append(
        {
            "role":
            "assistant",

            "content":
            reply
        }
    )

    with st.chat_message(
        "assistant"
    ):
        st.write(reply)