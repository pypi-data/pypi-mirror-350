from ai_cap_utils.agent import BaseAgent
from ai_cap_utils.streamlit import run_streamlit_chat_ui

if __name__ == "__main__":
    my_agent = BaseAgent(
        system_prompt="You are an extrovert who has a nice personality and loves to chat."
    )
    run_streamlit_chat_ui(my_agent)
