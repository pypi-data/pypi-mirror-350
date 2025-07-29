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


# --------------------------------------------
# Use a prebuilt agent to summarise content
# --------------------------------------------
sum_agent = SummariserAgent()
text = """
The concept of "digital minimalism" has gained popularity as a response to the overwhelming presence of technology in daily life.
It advocates for a more intentional and focused use of digital tools, rather than a constant and passive consumption of information.
Digital minimalists believe that by limiting time on social media, turning off non-essential notifications, and setting clear boundaries for screen use, individuals can regain control over their attention and mental well-being.

This philosophy doesn't call for abandoning technology altogether, but rather encourages a more mindful approach to its usage.
For example, instead of checking email constantly throughout the day, digital minimalists might schedule specific times to review and respond.
Similarly, instead of scrolling through social media feeds, they might use those moments for meaningful offline activities like reading, walking, or spending time with loved ones.

Research has shown that excessive screen time, especially on social media, is linked to increased levels of anxiety, depression, and reduced productivity.
Digital minimalism aims to counter these effects by promoting clarity, focus, and a more balanced lifestyle.
Ultimately, it's about making technology serve your values rather than letting it dictate your behavior.
"""

r = agent.chat_each_message(user_input=text, print_chat=True)
print()
print(r)  # Inspect the output

print()

# Test interactive chat
agent.chat_interact()
