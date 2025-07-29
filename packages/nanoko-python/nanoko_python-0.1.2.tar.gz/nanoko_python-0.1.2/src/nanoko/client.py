from httpx import Client, AsyncClient

from nanoko.api.llm import LLMAPI, AsyncLLMAPI
from nanoko.api.user import UserAPI, AsyncUserAPI
from nanoko.api.bank import BankAPI, AsyncBankAPI
from nanoko.api.service import ServiceAPI, AsyncServiceAPI


class Nanoko:
    """The client for the Nanoko API."""

    def __init__(self, base_url: str = "http://localhost:25324", client: Client = None):
        self.base_url = base_url
        self.client = client or Client()
        self.user = UserAPI(base_url, self.client)
        self.bank = BankAPI(base_url, self.client)
        self.llm = LLMAPI(base_url, self.client)
        self.service = ServiceAPI(base_url, self.client)


class AsyncNanoko:
    """The async client for the Nanoko API."""

    def __init__(
        self, base_url: str = "http://localhost:25324", client: AsyncClient = None
    ):
        self.base_url = base_url
        self.client = client or AsyncClient()
        self.user = AsyncUserAPI(base_url, self.client)
        self.bank = AsyncBankAPI(base_url, self.client)
        self.llm = AsyncLLMAPI(base_url, self.client)
        self.service = AsyncServiceAPI(base_url, self.client)
