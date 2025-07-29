import streamlit as st

from ai_cap_utils.agent._base import BaseAgent, BaseMultiAgentLLMRouter


def run_streamlit_chat_ui(agent: BaseAgent | BaseMultiAgentLLMRouter):
    """Runs a Streamlit chat UI with the specified agent
    
    Parameters
    ----------
        - agent (BaseAgent | BaseMultiAgentLLMRouter): An agent that can chat

    Usage
    -----
    You have to run `streamlit` command with this function.

    Example:

    In your main.py might look like this...
    

    ```python
    from ai_cap_utils.agent import BaseAgent
    from ai_cap_utils.streamlit import run_streamlit_chat_ui

    if __name__ == "__main__":
        my_agent = BaseAgent(
            system_prompt="You are an extrovert who has a nice personality and loves to chat."
        )
        run_streamlit_chat_ui(my_agent)
    ```

    Then, in command line, you must run

    ```
    streamlit run main.py
    ```
    """

    st.set_page_config(page_title="Agent Chat")
    st.title("Chat with Agent")

    # Initialise agent
    if "agent" not in st.session_state:
        st.session_state.agent = agent

    # Initialise message history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Print available messages right away
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    # Get the new user input
    user_input = st.chat_input("Say something...")
    if user_input:
        # Write the message to the chat box right away before waiting for AI response, and before re-render the page
        st.chat_message("user").write(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        response = st.session_state.agent.chat_each_message(user_input)

        # Get the latest AI message
        ai_state_messages = response[-1]["messages"]
        ai_message_content = ai_state_messages[-1].content

        st.chat_message("assistant").write(ai_message_content)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": ai_message_content}
        )
