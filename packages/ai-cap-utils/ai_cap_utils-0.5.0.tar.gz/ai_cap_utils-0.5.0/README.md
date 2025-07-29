# ai-cap-utils

A library to simplify your use case with chat bot with LLMs. Perfect for Common AI Platform.

## Installation
 ```
 uv add ai-cap-utils
 ```

## Usage

See `example.py` and `example_multiagents.py`.


### General/Chat agent with Python

```python
from ai_cap_utils.agent import BaseAgent
from ai_cap_utils.agent.prebuilt import SummariserAgent
from ai_cap_utils.tool import tool


# --------------------------------------------
# Create and run your own agent with some tool
# --------------------------------------------
@tool
def add_numbers(a: int, b: int):
    """Adds two numbers together"""
    return a + b


agent = BaseAgent(
    system_prompt="You are a helpful assistant that answers everything nicely (only that you can do or know)",
    tools=[add_numbers],
)
r = agent.chat_each_message("hello")
r = agent.chat_each_message("add two numbers for me")
r = agent.chat_each_message("2 and 4")
print(r)  # Inpect the output
print()

# You can use `chat_interact()` method to have an interactive session
agent.chat_interact()
```

Now, if you use `self.chat_interact()`, save the file and run this file in the command line.

```
uv run your_file.py
```

Or activate your python environment and run
```
python your_file.py
```

Example output:
```
================================ Human Message =================================

hello
================================== Ai Message ==================================

Hello! How can I assist you today?
================================ Human Message =================================

add two numbers for me
================================== Ai Message ==================================

Of course! Please provide the two numbers you'd like to add.
================================ Human Message =================================

2 and 4
================================== Ai Message ==================================
Tool Calls:
  add_numbers (call_kGDJ89gTwG6cTZFT7cWr1dBs)
 Call ID: call_kGDJ89gTwG6cTZFT7cWr1dBs
  Args:
    a: 2
    b: 4
================================= Tool Message =================================
Name: add_numbers

6
================================== Ai Message ==================================

The sum of 2 and 4 is 6.
```

Initialise an agent using a Google's credentials dict

```python
from ai_cap_utils.tool import tool
from ai_cap_utils.agent import BaseAgent

# --------------------------------------------
# Import some pre-defined agent
# --------------------------------------------
sum_agent = SummariserAgent()


# --------------------------------------------
# Create your own math agent
# --------------------------------------------
@tool
def add_numbers(a: int, b: int):
    """Add two numbers together"""
    return a + b


@tool
def multiplication(a: float, b: float):
    """Multiply two numbers together"""
    return a * b


math_system_prompt = "You are a specialist in math problems, you can add and multiply."

# Get a dictionary somehow... (Usually, you can pass a path to your credentials.json)
# But if the credentials are retreived from a secret manager, you can pass in directly.
google_creds = {
    "type": "service_account",
    "project_id": "random-project",
    "private_key_id": "your-private-key",
    "private_key": "-----BEGIN PRIVATE KEY-----\nsome-random-gibberish\n-----END PRIVATE KEY-----\n",
    "client_email": "user@random-project.iam.gserviceaccount.com",
    "client_id": "12345678910",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/roojai%40random-project.iam.gserviceaccount.com",
}

math_agent = BaseAgent(
    system_prompt=math_system_prompt,
    tools=[add_numbers, multiplication],
    google_credentials_path=google_creds,
)
```

### Streamlit chat UI

We also provide a function that runs the chat UI with your pre-defined agent: `run_streamlit_chat_ui(agent)`.

The function is under `ai_cap_utils.streamlit`.

Let's say your `main.py` looks like this:

```python
from ai_cap_utils.agent import BaseAgent
from ai_cap_utils.streamlit import run_streamlit_chat_ui

if __name__ == "__main__":
    my_agent = BaseAgent(
        system_prompt="You are an extrovert who has a nice personality and loves to chat."
    )
    run_streamlit_chat_ui(my_agent)  # This command runs the streamlit chat UI and wait for the streamlit run command
```

You must run the `streamlit` command in the terminal/CLI:

```
streamlit run main.py
```

Or if you use `uv`:

```
uv run streamlit run main.py
```