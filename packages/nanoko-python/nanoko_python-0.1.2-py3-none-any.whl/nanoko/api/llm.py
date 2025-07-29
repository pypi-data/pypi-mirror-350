from httpx import Client, AsyncClient


class LLMAPI:
    """The API for the LLM."""

    def __init__(self, base_url: str = "http://localhost:25324", client: Client = None):
        self.base_url = base_url
        self.client = client or Client()

    def get_hint(self, sub_question_id: int, question: str) -> str:
        """Get a hint for the sub-question.

        Args:
            sub_question_id (int): The ID of the sub-question.
            question (str): The question to ask.

        Returns:
            str: The hint for the sub-question.
        """
        params = {
            "sub_question_id": sub_question_id,
            "question": question,
        }
        response = self.client.get(f"{self.base_url}/api/v1/llm/hint", params=params)
        response.raise_for_status()
        return response.json()["hint"]


class AsyncLLMAPI:
    """The async API for the LLM."""

    def __init__(
        self, base_url: str = "http://localhost:25324", client: AsyncClient = None
    ):
        self.base_url = base_url
        self.client = client or AsyncClient()

    async def get_hint(self, sub_question_id: int, question: str) -> str:
        """Get a hint for the sub-question.

        Args:
            sub_question_id (int): The ID of the sub-question.
            question (str): The question to ask.

        Returns:
            str: The hint for the sub-question.
        """
        params = {
            "sub_question_id": sub_question_id,
            "question": question,
        }
        response = await self.client.get(
            f"{self.base_url}/api/v1/llm/hint", params=params
        )
        response.raise_for_status()
        return response.json()["hint"]
