import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import load_prompt

api_key = st.secrets.get("GOOGLE_API_KEY")
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)


st.sidebar.title("AI Soulmate")
st.sidebar.subheader("Made with love for you 💖")
gender = st.sidebar.radio("Gender", ["Male", "Female"], horizontal=True)
age = st.sidebar.selectbox("Age", ["Select", "Teenage", "Young", "Old"])

prompt_template = load_prompt("template.json")

system_prompt_text = prompt_template.format(gender=gender, age=age)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content=system_prompt_text)]


for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)

user_input = st.chat_input("You:")
if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.chat_message("user").write(user_input)
    result = model.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(AIMessage(content=result.content))
    st.chat_message("assistant").write(result.content)
