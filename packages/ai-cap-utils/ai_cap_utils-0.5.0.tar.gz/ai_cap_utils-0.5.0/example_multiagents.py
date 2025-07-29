from ai_cap_utils.tool import tool
from ai_cap_utils.agent.base import BaseMultiAgentLLMRouter, BaseAgent
from ai_cap_utils.agent.prebuilt import SummariserAgent

# --------------------------------------------
# Import some pre-defined agent
# --------------------------------------------
sum_agent = SummariserAgent()

# --------------------------------------------
# Create and run your own math agent
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

math_agent = BaseAgent(system_prompt=math_system_prompt, tools=[add_numbers, multiplication])


# --------------------------------------------
# Connect the agents together using the router
# --------------------------------------------
router_agent = BaseMultiAgentLLMRouter([sum_agent, math_agent])


# --------------------------------------------
# Test chat
# --------------------------------------------
text = """
Summarise this please:

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

r = router_agent.chat_each_message("Summarise this text for me")
r = router_agent.chat_each_message(text)
print(r)  # Inspect results
print()

r = router_agent.chat_each_message("Can you multiply 4 with 8?")
print(r)  # Inspect results
print()

print("Now, let's chat with this MultiAgent router...")
router_agent.chat_interact()  # Interactive chat