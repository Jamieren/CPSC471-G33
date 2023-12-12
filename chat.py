from streamlit_extras.stateful_chat import chat, add_message
import streamlit as st
import time 
def example():
    st.session_state["username"] = st.session_state["username"]
    with chat(key="my_chat"):
        if prompt := st.chat_input():
            add_message("user", prompt, avatar="🧑")

            def stream_echo():
                for word in prompt.split():
                    yield word + " "
                    time.sleep(0.15)

            add_message("assistant", "Therapist: ", stream_echo, avatar="👩‍⚕️")
example()