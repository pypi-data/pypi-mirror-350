# arpakit

import asyncio
import logging

import httpx
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion

from arpakitlib.ar_logging_util import setup_normal_logging

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

"""
https://platform.openai.com/docs/
"""


class OpenAIAPIClient:
    def __init__(
            self,
            *,
            open_ai: OpenAI,
            async_open_ai: AsyncOpenAI
    ):
        self._logger = logging.getLogger(self.__class__.__name__)

        self.open_ai = open_ai
        self.async_open_ai = async_open_ai

    def check_conn(self):
        self.open_ai.models.list()

    def is_conn_good(self) -> bool:
        try:
            self.check_conn()
            return True
        except Exception as e:
            self._logger.error(e)
        return False

    async def async_check_conn(self):
        await self.async_open_ai.models.list()

    async def async_is_conn_good(self) -> bool:
        try:
            await self.async_check_conn()
            return True
        except Exception as e:
            self._logger.error(e)
        return False

    def simple_ask(
            self,
            *,
            prompt: str | None = None,
            content: str,
            model: str = "gpt-4o",
            max_tokens: int = 300
    ) -> ChatCompletion:
        messages = []
        if prompt is not None:
            messages.append({
                "role": "system",
                "content": prompt
            })
        messages.append({
            "role": "user",
            "content": content
        })
        response: ChatCompletion = self.open_ai.chat.completions.create(
            model=model,
            messages=messages,
            n=1,
            temperature=0.1,
            top_p=0.9,
            max_tokens=max_tokens
        )
        return response

    async def async_simple_ask(self, *, prompt: str | None = None, string: str) -> ChatCompletion:
        messages = []
        if prompt is not None:
            messages.append({
                "role": "system",
                "content": prompt
            })
        messages.append({
            "role": "user",
            "content": string
        })
        response: ChatCompletion = await self.async_open_ai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            n=1,
            temperature=0.1,
            top_p=0.9,
            max_tokens=300
        )
        return response


def __example():
    pass


async def __async_example():
    setup_normal_logging()
    api_key = ""
    base_url = "https://api.proxyapi.ru/openai/v1"
    client = OpenAIAPIClient(
        open_ai=OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=httpx.Timeout(
                timeout=60,
            )
        ),
        async_open_ai=AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=httpx.Timeout(
                timeout=60,
            )
        )
    )

    print(await client.async_is_conn_good())

    response = client.simple_ask(
        content="Привет, проверяю тебя"
    )
    print(response.choices[0].message.content)


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
