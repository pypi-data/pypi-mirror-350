from uuid import uuid4

import coolname
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.chat_models.openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from ..state import MessageState
from ..type import DestinationModelType, MessageDict
from ..utils.envcreds import _set_google_credentials, _set_openai_key

load_dotenv()


class BaseChatInterface:
    def chat_each_message(
        self,
        user_input: str,
        thread_id: str = "1",
        print_chat: bool = True,
    ) -> list[MessageDict]:
        """Send one message to the LLM in stream mode and returns list of messages history

        Paramaters
        ----------
            - user_input (str): A message string to send to the Agent's LLM

            - thread_id (str): The thread ID for memory (Default = "1")

            - print_chat (bool): Whether or not to pretty print the chats (Default = True)

        Returns
        -------
            list[MessageDict]:
                A list of messages dict history

                For example,
                ```
                [
                    {"messages": [HumanMessage()]},
                    {"messages": [HumanMessage(), AIMessage()]}
                ]
                ```
        """

        input_messages = []
        if self.system_prompt and not self._has_system_prompt_in_history:
            input_messages.append({"role": "system", "content": self.system_prompt})
            self._has_system_prompt_in_history = True

        input_messages.append({"role": "user", "content": user_input})

        config = {"configurable": {"thread_id": thread_id}}
        events = self.graph.stream(
            {"messages": input_messages}, config, stream_mode="values"
        )

        # Events is a list of message dict [{"message": [HumanMessage(), AIMessage()]}, {"message": [...]}]

        ret_msgs = []

        if print_chat:
            for event in events:
                msg = event["messages"]
                msg[-1].pretty_print()
                ret_msgs.append(event)

        return ret_msgs

    def run_batch(self, messages: list[str], thread_id: str = "1") -> MessageDict:
        """Runs a list of messages to the Agent's LLM and returns a message dict

        Parameters
        ----------
            - messages (list[str]): A list of messages to send to LLM

            - thread_id (str): The thread ID for memory (Default = "1")

        Returns
        -------
            MessageDict:
                A message dictionary in the form of {"message": [HumanMessage(), ...]}
        """
        config = {"configurable": {"thread_id": thread_id}}
        return self.graph.invoke({"messages": messages}, config)

    def chat_interact(self, thread_id: str = "1") -> None:
        """A function to interact/chat with the Agent's LLM

        Parameters
        ----------
            - thread_id (str): The thread ID for memory (Default = "1")

        Returns
        -------
            None
        """

        while True:
            try:
                user_input = input("User: ")
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break

                self.chat_each_message(
                    user_input=user_input, thread_id=thread_id, print_chat=True
                )

            except Exception:
                # fallback
                print("===================================================")
                print("An Exception has occurred, the chat loop has ended.")
                print("===================================================")
                break


class BaseAgent(BaseChatInterface):
    def __init__(
        self,
        system_prompt: str,
        model: str = "poc-ai-gcp-vertex-gemini-2.0-flash",
        model_provider: str = "cap-litellm",
        base_url: str = "https://do-cap-litellm-dev.scg-wedo.tech",
        tools: list[BaseTool] | None = None,
        temperature: float = 0,
        agent_name: str | None = None,
        google_credentials: str | dict | None = None,
        openai_api_key: str | None = None,
    ):
        """BaseAgent that can chat/interact and also route to some pre-defined tools

        Parameters
        ----------
            - system_prompt (str): A system prompt for the Agent. (Mandatory) Explain what this agent does or specialised in.

            - model (str): An LLM's model name (Default = "poc-ai-gcp-vertex-gemini-2.0-flash")

                The name of the model, e.g. "o3-mini", "claude-3-5-sonnet-latest". You can also specify model and model provider in a single argument using '{model_provider}:{model}' format, e.g. "openai:gpt-4o".

            - model_provider (str): The provider for the model (Default = "litellm")

                If not specified as part of model arg (see above), will attempt to infer model_provider from the model.

            - base_url (str): The base url for our lite-llm server

            - tools (list[BaseTool] | None): A list of tools to register to the Agent (Default = None)

            - temperature (float): Temperature parameter for the LLM (Default = 0)

            - agent_name (str): A name for the agent instance (Default = None)

                If not provided, default to using the class name, appended with random words and 4 characters of uuid4().

            - google_credentials (str | dict | None): Path to credentials.json file or a dictionary of the Google's credentials format that allows you to connect with Google's LLM models (Default = None)

                If None, it will try to find `GOOGLE_APPLICATION_CREDENTIALS` key in the system environment variables.

            - openai_api_key (str | None): API key/token for Open AI models (`model_provider = "openai"`) (Default = None)

                If None, it will try to find `OPENAI_API_KEY` key in the system environment variables.

                If the `model_provider` is "litellm", meaning our own API endpoint, this key must be provided.
                (Our endpoint uses openai standard)

        Notes
        -----
        This class has the following main methods:

        `self.chat_each_message()`: Sends each message to the Agent's LLM and returns a message history

        `self.run_batch()`: Invoke the Agent's LLM by sending a list of messages to the LLM

        `self.chat_interact()`: A function to interact/chat with the Agent's LLM
        """

        self.system_prompt = system_prompt
        self.tools = tools or []
        self._has_system_prompt_in_history = False
        self.memory = MemorySaver()

        # Define a name for the instance
        if agent_name:
            self.agent_name = agent_name
        else:
            self.agent_name = f"{type(self).__name__} - {coolname.generate_slug(2).split('-')[0]}-{str(uuid4())[:4]}"

        # Litellm endpoint
        self._endpoint = base_url

        # Credentials
        self.__google_credentials = google_credentials
        self.__openai_api_key = openai_api_key
        self._set_credentials()

        if model_provider == "cap-litellm":
            if openai_api_key is None:
                raise ValueError(
                    "`openai_api_key` must not be None if you want to use litellm."
                )

            self.llm = ChatOpenAI(
                model=model,
                base_url=self._endpoint,
                api_key=openai_api_key,
                temperature=temperature,
                streaming=True,
            )
            
        else:
            self.llm = init_chat_model(
                model=model,
                model_provider=model_provider,
                temperature=temperature,
                streaming=True,
            )

        self.graph = self._build_graph()

    def _set_credentials(self):
        """Sets credentials to os.environ for the supported clouds"""

        _set_google_credentials(google_credentials=self.__google_credentials)
        _set_openai_key(openai_api_key=self.__openai_api_key)

    def _build_graph(self) -> CompiledStateGraph:
        """Builds the graph for this Agent"""

        graph_builder = StateGraph(MessageState)

        if self.tools:
            tool_node = ToolNode(tools=self.tools)
            self.llm = self.llm.bind_tools(tools=self.tools)

        def chatbot(state: MessageState):
            return {"messages": [self.llm.invoke(state["messages"])]}

        # Build Nodes
        graph_builder.add_node("chatbot", chatbot)

        if self.tools:
            graph_builder.add_node("tools", tool_node)

        # Build edges
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)

        if self.tools:
            graph_builder.add_conditional_edges(
                "chatbot", tools_condition, {"tools": "tools", END: END}
            )
            graph_builder.add_edge("tools", "chatbot")

        return graph_builder.compile(checkpointer=self.memory)

    def rebuild_graph_with_memory(self, memory: MemorySaver):
        self.memory = memory
        self.graph = self._build_graph()


class BaseMultiAgentLLMRouter(BaseChatInterface):
    def __init__(
        self,
        agents_list: list[BaseAgent],
        model: str = "gpt-4o-mini",
        model_provider: str = None,
        google_credentials: str | dict | None = None,
        openai_api_key: str | None = None,
    ):
        """BaseAgent that can chat/interact and also route to some pre-defined tools

        Parameters
        ----------
            - agents_list (list[BaseAgent]): A list of `BaseAgent`s you want to connect/route to

            - model (str): An LLM's model name (Default = "gpt-4o-mini")

                The name of the model, e.g. "o3-mini", "claude-3-5-sonnet-latest". You can also specify model and model provider in a single argument using '{model_provider}:{model}' format, e.g. "openai:gpt-4o".

            - model_provider (str): The provider for the model (Default = None)

                If not specified as part of model arg (see above), will attempt to infer model_provider from the model.


            - google_credentials (str | None): Path to credentials.json file or a dictionary of the Google's credentials format that allows you to connect with Google's LLM models (Default = None)

                If None, it will try to find `GOOGLE_APPLICATION_CREDENTIALS` key in the system environment variables.

            - openai_api_key (str | None): API key/token for Open AI models (`model_provider = "openai"`) (Default = None)

                If None, it will try to find `OPENAI_API_KEY` key in the system environment variables.

        Notes
        -----
        This class has the following main methods:

        `self.chat_each_message()`: Sends each message to the Agent's LLM and returns a message history

        `self.run_batch()`: Invoke the Agent's LLM by sending a list of messages to the LLM

        `self.chat_interact()`: A function to interact/chat with the Agent's LLM
        """

        self.agents_list = agents_list
        self.agents_names: list[str] = [agent.agent_name for agent in self.agents_list]

        # No system prompt...
        self.system_prompt = None
        self._has_system_prompt_in_history = False

        # Credentials
        self.__google_credentials = google_credentials
        self.__openai_api_key = openai_api_key
        self._set_credentials()

        self.llm = init_chat_model(
            model=model,
            model_provider=model_provider,
            streaming=False,
        ).with_structured_output(DestinationModelType)

        self.shared_memory = MemorySaver()

        # Build router graph
        self.graph = self._build_router_graph()

    def _set_credentials(self):
        """Sets credentials to os.environ for the supported clouds"""

        _set_google_credentials(google_credentials=self.__google_credentials)
        _set_openai_key(openai_api_key=self.__openai_api_key)

    def _build_router_graph(self):
        """Builds an LLM-based router graph"""

        description_lines = []

        # Rebuild each agent with the shared memory and get their description
        for agent in self.agents_list:
            agent.rebuild_graph_with_memory(self.shared_memory)
            description_lines.append(f"{agent.agent_name}: {agent.system_prompt}")

        description_str = "\n".join(description_lines)

        def route(state: MessageState) -> str:
            system_prompt = (
                "Objective: You must choose exactly one node name from the following list:\n"
                f"{', '.join(self.agents_names)}\n\n"
                "Here are brief descriptions of each node:\n"
                f"{description_str}\n\n"
                "You must output JSON in the format:\n"
                '{ "target": "<ONE_OF_THE_NODE_NAMES>" }\n'
                "Do not include any other fields."
            )

            # Prepare message
            # fmt: off
            messages = [{"role": "system", "content": system_prompt}] + state["messages"]
            # messages_trimmed = trim_tool_messages(messages)
            # fmt: on

            # result will be a pydantic class with a property `target`
            result = self.llm.invoke(messages)

            chosen_agent = result.target
            if chosen_agent in self.agents_names:
                print(f"LLM picked agent: {chosen_agent}")
                return chosen_agent
            else:
                print(f"Invalid choice: {chosen_agent}. Going to END.")
                return END

        multi_agent_graph = StateGraph(MessageState)

        # Add each agent node and connect to END
        for agent_name, agent in zip(self.agents_names, self.agents_list):
            multi_agent_graph.add_node(agent_name, agent.graph)
            multi_agent_graph.add_edge(agent_name, END)

        multi_agent_graph.add_conditional_edges(START, route)

        return multi_agent_graph.compile(self.shared_memory)
