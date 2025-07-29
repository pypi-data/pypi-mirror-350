from ._base import BaseAgent


system_prompt = """You are a helpful assistant that answers everything nicely (only that you can do or know)
You are an English only assistant. Please answer in English only"""


class EnglishAgent(BaseAgent):
    def __init__(
        self,
        model: str = "gpt-4o",
        model_provider: str = "openai",
        agent_name: str | None = None,
        google_credentials: str | None = None,
        openai_api_key: str | None = None,
    ):
        super().__init__(
            system_prompt=system_prompt,
            model=model,
            model_provider=model_provider,
            tools=None,
            temperature=0,
            agent_name=agent_name,
            google_credentials=google_credentials,
            openai_api_key=openai_api_key,
        )


system_prompt = "คุณเป็นผู้ช่วยที่นิสัยดี อัธยาศัยดี ให้ความช่วยเหลือเป็นภาษาไทยเท่านั้น ตอบคำถาม และแนะนำอย่างสุภาพ โดยสุดความสามารถ"


class ThaiAgent(BaseAgent):
    def __init__(
        self,
        model: str = "gpt-4o",
        model_provider: str = "openai",
        agent_name: str | None = None,
        google_credentials: str | None = None,
        openai_api_key: str | None = None,
    ):
        super().__init__(
            system_prompt=system_prompt,
            model=model,
            model_provider=model_provider,
            tools=None,
            temperature=0,
            agent_name=agent_name,
            google_credentials=google_credentials,
            openai_api_key=openai_api_key,
        )


system_prompt = """You are a summariser. You summarise everything into concise, cohesive and comprehensive content where your customers can appreciate and understand everything easily.
Summarise everything in a nice manner. And do not make stuff up. Base everything from the evidence you gathered. The length of the output should be less than the original content.
"""


class SummariserAgent(BaseAgent):
    def __init__(
        self,
        model: str = "gpt-4o",
        model_provider: str = "openai",
        agent_name: str | None = None,
        google_credentials: str | None = None,
        openai_api_key: str | None = None,
    ):
        super().__init__(
            system_prompt=system_prompt,
            model=model,
            model_provider=model_provider,
            tools=None,
            temperature=0,
            agent_name=agent_name,
            google_credentials=google_credentials,
            openai_api_key=openai_api_key,
        )
