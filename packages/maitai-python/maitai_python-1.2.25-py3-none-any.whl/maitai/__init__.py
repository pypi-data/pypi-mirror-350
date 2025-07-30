from maitai._context import ContextManager
from maitai._maitai import Chat, Maitai
from maitai._maitai_async import MaitaiAsync

chat = Chat()
context = ContextManager()
AsyncOpenAI = MaitaiAsync
OpenAI = Maitai

AsyncMaitai = MaitaiAsync


def initialize(api_key):
    from maitai._config import config

    config.initialize(api_key)
