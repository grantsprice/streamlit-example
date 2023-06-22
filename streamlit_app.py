import openai
import streamlit as st
from streamlit_chat import message

with st.sidebar:
    #openai_api_key = st.text_input('OpenAI API Key',key='chatbot_api_key')
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Streamlit GPT")
openai_api_key = st.secrets["chatbot_api_key"]
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    a.text('Enter your name')
    user_input = a.text_input(
        label="Your message:",
        placeholder="What should we call you?",
        label_visibility="collapsed",
    )
    a.text('What do you do?')
    user_occupation = a.text_input(
        label="What is your occupation?",
        placeholder="Firefighter!",
        label_visibility="collapsed",
    )
    a.text('How old are you?')
    user_age = a.text_input(
        label="What is your age?",
        placeholder="Enter age...",
        label_visibility="collapsed",
    )
    a.text('What sort of physical activity do you do?')
    user_physical = a.text_input(
        label="What sort of physical activity do you do?",
        placeholder="Olympic swimmer?",
        label_visibility="collapsed",
    )
    b.form_submit_button("Send", use_container_width=True)

for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")

if user_input and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    
if user_input and openai_api_key:
    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": "Give me a life prediction based on the following: "})
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "user", "content": "My occupation is "})
    st.session_state.messages.append({"role": "user", "content": user_occupation})
    st.session_state.messages.append({"role": "user", "content": "I am "+user_age+" years old"})
    st.session_state.messages.append({"role": "user", "content": user_physical})
    message("Sharing life story...", is_user=True)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    message(msg.content)
