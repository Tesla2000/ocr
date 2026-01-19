from typing import Optional

from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import Field
from pydantic import SecretStr


class TextCleanup(BaseModel):
    openai_api_key: Optional[SecretStr] = None
    client: ChatOpenAI = Field(
        default_factory=lambda validated_data: ChatOpenAI(
            model="gpt-4.1-mini", api_key=validated_data["openai_api_key"]
        )
    )
    system_prompt: str = """You are a text cleanup assistant. Your task is to:
1. Fix OCR mistakes and typos
2. Remove page numbers
3. Remove chapter titles and headers
4. Remove footers and repeated elements
5. Preserve the actual content and maintain proper paragraph structure
6. Fix formatting issues

Return only the cleaned text without any explanations or metadata. You will be given text in polish

Before:
Łatwość poznawcza
A powtarzajare de
przez szata graficzna
utorowana idea
dobry nastrój
5. Łatwość poznawcza
uczucie prawdziwości
ATWOŚC
uczucie przyjemności
uczucie larwości
83
na wiele
Za kandym razem, kiedy to sobie uświadamiasz - a może nawet wte.
kiedy sobie nie uświadamiasz - w twoim mózgu dokonują się
operacie mające utrzymywać i aktualizować odpowiedzi
wanych pytan: Czy dzieje się coś nowego? Czy coś mi grozi? Czy
wko w porzadku? Czy nie trzeba zwrócić uwagi na coś innego?

After:
Za każdym razem, kiedy to sobie uświadamiasz - a może nawet wtedy
kiedy sobie nie uświadamiasz - w twoim mózgu dokonują się
operacie mające utrzymywać i aktualizować odpowiedzi
ważnych pytań: Czy dzieje się coś nowego? Czy coś mi grozi? Czy
wszystko w porzadku? Czy nie trzeba zwrócić uwagi na coś innego?
    """

    async def cleanup_text(self, text: str) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=text),
        ]
        response = await self.client.ainvoke(messages)
        return response.content
