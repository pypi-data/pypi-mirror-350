from pathlib import Path
from httpx import Client, AsyncClient
from typing import List, Optional, BinaryIO, Union

from nanoko.models.question import Question, ConceptType, ProcessType


class BankAPI:
    """The API for the bank."""

    def __init__(self, base_url: str = "http://localhost:25324", client: Client = None):
        self.base_url = base_url
        self.client = client or Client()

    def upload_image(
        self, file: Union[Path, str, BinaryIO, bytes], content_type: str = "image/png"
    ) -> str:
        """Upload an image to the server and return its hash.

        Args:
            file (Union[Path, str, BinaryIO, bytes]): The image file to upload.
            content_type (str): The content type of the image. Defaults to "image/png".
        Returns:
            str: The hash of the uploaded image.
        """
        if isinstance(file, str):
            file = Path(file)
        if isinstance(file, Path):
            file = file.read_bytes()
        if isinstance(file, bytes):
            files = {
                "file": (f"image.{content_type.split('/')[1]}", file, content_type)
            }
        elif isinstance(file, BinaryIO):
            files = {
                "file": (
                    f"image.{content_type.split('/')[1]}",
                    file.read(),
                    content_type,
                )
            }
        else:
            raise ValueError("Invalid file type")

        response = self.client.post(
            f"{self.base_url}/api/v1/bank/image/upload", files=files
        )
        response.raise_for_status()
        return response.json()["hash"]

    def add_image(self, description: str, hash: str) -> int:
        """Add an image to the database.

        Args:
            description (str): The description of the image.
            hash (str): The hash of the image.

        Returns:
            int: The id of the image in the database.
        """
        data = {
            "description": description,
            "hash": hash,
        }
        response = self.client.post(f"{self.base_url}/api/v1/bank/image/add", json=data)
        response.raise_for_status()
        return response.json()["image_id"]

    def set_image_description(self, image_id: int, description: str) -> dict:
        """Set the description of an image.

        Args:
            image_id (int): The id of the image.
            description (str): The new description of the image.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "image_id": image_id,
            "description": description,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/bank/image/set/description", json=data
        )
        response.raise_for_status()
        return response.json()

    def set_image_hash(self, image_id: int, hash: str) -> dict:
        """Set the hash of an image.

        Args:
            image_id (int): The id of the image.
            hash (str): The new hash of the image.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "image_id": image_id,
            "hash": hash,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/bank/image/set/hash", json=data
        )
        response.raise_for_status()
        return response.json()

    def get_image_description(self, image_id: int) -> str:
        """Get the description of an image.

        Args:
            image_id (int): The id of the image.

        Returns:
            str: The description of the image.
        """
        response = self.client.get(
            f"{self.base_url}/api/v1/bank/image/get/description",
            params={"image_id": image_id},
        )
        response.raise_for_status()
        return response.json()["description"]

    def get_image(self, image_id: int) -> bytes:
        """Get an image from the database.

        Args:
            image_id (int): The id of the image.

        Returns:
            bytes: The image file.
        """
        response = self.client.get(
            f"{self.base_url}/api/v1/bank/image/get", params={"image_id": image_id}
        )
        response.raise_for_status()
        return response.content

    def add_question(self, question: Question) -> int:
        """Add a question to the database.

        Args:
            question (Question): The question to add.

        Returns:
            int: The id of the question in the database.
        """
        response = self.client.post(
            f"{self.base_url}/api/v1/bank/question/add", json=question.model_dump()
        )
        response.raise_for_status()
        return response.json()["question_id"]

    def set_sub_question_description(
        self, sub_question_id: int, description: str
    ) -> dict:
        """Set the description of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            description (str): The new description of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "description": description,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/description",
            json=data,
        )
        response.raise_for_status()
        return response.json()

    def set_sub_question_options(
        self, sub_question_id: int, options: List[str]
    ) -> dict:
        """Set the options of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            options (List[str]): The new options of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "options": options,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/options", json=data
        )
        response.raise_for_status()
        return response.json()

    def set_sub_question_answer(self, sub_question_id: int, answer: str) -> dict:
        """Set the answer of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            answer (str): The new answer of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "answer": answer,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/answer", json=data
        )
        response.raise_for_status()
        return response.json()

    def set_sub_question_concept(
        self, sub_question_id: int, concept: ConceptType
    ) -> dict:
        """Set the concept of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            concept (ConceptType): The new concept of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "concept": concept.value,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/concept", json=data
        )
        response.raise_for_status()
        return response.json()

    def set_sub_question_process(
        self, sub_question_id: int, process: ProcessType
    ) -> dict:
        """Set the process of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            process (ProcessType): The new process of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "process": process.value,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/process", json=data
        )
        response.raise_for_status()
        return response.json()

    def set_sub_question_keywords(
        self, sub_question_id: int, keywords: List[str]
    ) -> dict:
        """Set the keywords of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            keywords (List[str]): The new keywords of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "keywords": keywords,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/keywords", json=data
        )
        response.raise_for_status()
        return response.json()

    def set_sub_question_image(self, sub_question_id: int, image_id: int) -> dict:
        """Set the image of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            image_id (int): The id of the image.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "image_id": image_id,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/image", json=data
        )
        response.raise_for_status()
        return response.json()

    def delete_sub_question_image(self, sub_question_id: int) -> dict:
        """Delete the image of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        response = self.client.delete(
            f"{self.base_url}/api/v1/bank/sub-question/delete/image",
            params={"sub_question_id": sub_question_id},
        )
        response.raise_for_status()
        return response.json()

    def get_questions(
        self,
        question_id: Optional[int] = None,
        source: Optional[str] = None,
        concept: Optional[ConceptType] = None,
        process: Optional[ProcessType] = None,
    ) -> List[Question]:
        """Get questions from the database.

        Args:
            question_id (Optional[int], optional): The question id of the question. Defaults to None.
            source (Optional[str], optional): The source of the question. Defaults to None.
            concept (Optional[ConceptType], optional): The concept of questions. Defaults to None.
            process (Optional[ProcessType], optional): The process of questions. Defaults to None.

        Returns:
            List[Question]: The list of questions.
        """
        params = {}
        if question_id is not None:
            params["question_id"] = question_id
        if source is not None:
            params["source"] = source
        if concept is not None:
            params["concept"] = concept.value
        if process is not None:
            params["process"] = process.value

        response = self.client.get(
            f"{self.base_url}/api/v1/bank/question/get", params=params
        )
        response.raise_for_status()
        return [Question.model_validate(q) for q in response.json()]

    def approve_question(self, question_id: int) -> dict:
        """Approve a question in the database.

        Args:
            question_id (int): The id of the question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "question_id": question_id,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/bank/question/approve", json=data
        )
        response.raise_for_status()
        return response.json()

    def delete_question(self, question_id: int) -> dict:
        """Delete a question in the database.

        Args:
            question_id (int): The id of the question.

        Returns:
            dict: The result of the operation.
        """
        response = self.client.delete(
            f"{self.base_url}/api/v1/bank/question/delete",
            params={"question_id": question_id},
        )
        response.raise_for_status()
        return response.json()


class AsyncBankAPI:
    """The async API for the bank."""

    def __init__(
        self, base_url: str = "http://localhost:25324", client: AsyncClient = None
    ):
        self.base_url = base_url
        self.client = client or AsyncClient()

    async def upload_image(
        self, file: Union[Path, str, BinaryIO, bytes], content_type: str = "image/png"
    ) -> str:
        """Upload an image to the server and return its hash.

        Args:
            file (Union[Path, str, BinaryIO, bytes]): The image file to upload.
            content_type (str): The content type of the image. Defaults to "image/png".

        Returns:
            str: The hash of the uploaded image.
        """
        if isinstance(file, str):
            file = Path(file)
        if isinstance(file, Path):
            file = file.read_bytes()
        if isinstance(file, bytes):
            files = {
                "file": (f"image.{content_type.split('/')[1]}", file, content_type)
            }
        elif isinstance(file, BinaryIO):
            files = {
                "file": (
                    f"image.{content_type.split('/')[1]}",
                    file.read(),
                    content_type,
                )
            }
        else:
            raise ValueError("Invalid file type")

        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/image/upload", files=files
        )
        response.raise_for_status()
        return response.json()["hash"]

    async def add_image(self, description: str, hash: str) -> int:
        """Add an image to the database.

        Args:
            description (str): The description of the image.
            hash (str): The hash of the image.

        Returns:
            int: The id of the image in the database.
        """
        data = {
            "description": description,
            "hash": hash,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/image/add", json=data
        )
        response.raise_for_status()
        return response.json()["image_id"]

    async def set_image_description(self, image_id: int, description: str) -> dict:
        """Set the description of an image.

        Args:
            image_id (int): The id of the image.
            description (str): The new description of the image.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "image_id": image_id,
            "description": description,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/image/set/description", json=data
        )
        response.raise_for_status()
        return response.json()

    async def set_image_hash(self, image_id: int, hash: str) -> dict:
        """Set the hash of an image.

        Args:
            image_id (int): The id of the image.
            hash (str): The new hash of the image.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "image_id": image_id,
            "hash": hash,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/image/set/hash", json=data
        )
        response.raise_for_status()
        return response.json()

    async def get_image_description(self, image_id: int) -> str:
        """Get the description of an image.

        Args:
            image_id (int): The id of the image.

        Returns:
            str: The description of the image.
        """
        response = await self.client.get(
            f"{self.base_url}/api/v1/bank/image/get/description",
            params={"image_id": image_id},
        )
        response.raise_for_status()
        return response.json()["description"]

    async def get_image(self, image_id: int) -> bytes:
        """Get an image from the database.

        Args:
            image_id (int): The id of the image.

        Returns:
            bytes: The image file.
        """
        response = await self.client.get(
            f"{self.base_url}/api/v1/bank/image/get", params={"image_id": image_id}
        )
        response.raise_for_status()
        return response.content

    async def add_question(self, question: Question) -> int:
        """Add a question to the database.

        Args:
            question (Question): The question to add.

        Returns:
            int: The id of the question in the database.
        """
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/question/add", json=question.model_dump()
        )
        response.raise_for_status()
        return response.json()["question_id"]

    async def set_sub_question_description(
        self, sub_question_id: int, description: str
    ) -> dict:
        """Set the description of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            description (str): The new description of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "description": description,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/description",
            json=data,
        )
        response.raise_for_status()
        return response.json()

    async def set_sub_question_options(
        self, sub_question_id: int, options: List[str]
    ) -> dict:
        """Set the options of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            options (List[str]): The new options of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "options": options,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/options", json=data
        )
        response.raise_for_status()
        return response.json()

    async def set_sub_question_answer(self, sub_question_id: int, answer: str) -> dict:
        """Set the answer of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            answer (str): The new answer of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "answer": answer,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/answer", json=data
        )
        response.raise_for_status()
        return response.json()

    async def set_sub_question_concept(
        self, sub_question_id: int, concept: ConceptType
    ) -> dict:
        """Set the concept of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            concept (ConceptType): The new concept of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "concept": concept.value,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/concept", json=data
        )
        response.raise_for_status()
        return response.json()

    async def set_sub_question_process(
        self, sub_question_id: int, process: ProcessType
    ) -> dict:
        """Set the process of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            process (ProcessType): The new process of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "process": process.value,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/process", json=data
        )
        response.raise_for_status()
        return response.json()

    async def set_sub_question_keywords(
        self, sub_question_id: int, keywords: List[str]
    ) -> dict:
        """Set the keywords of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            keywords (List[str]): The new keywords of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "keywords": keywords,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/keywords", json=data
        )
        response.raise_for_status()
        return response.json()

    async def set_sub_question_image(self, sub_question_id: int, image_id: int) -> dict:
        """Set the image of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.
            image_id (int): The id of the image.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "sub_question_id": sub_question_id,
            "image_id": image_id,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/sub-question/set/image", json=data
        )
        response.raise_for_status()
        return response.json()

    async def delete_sub_question_image(self, sub_question_id: int) -> dict:
        """Delete the image of a sub-question.

        Args:
            sub_question_id (int): The id of the sub-question.

        Returns:
            dict: The result of the operation.
        """
        response = await self.client.delete(
            f"{self.base_url}/api/v1/bank/sub-question/delete/image",
            params={"sub_question_id": sub_question_id},
        )
        response.raise_for_status()
        return response.json()

    async def get_questions(
        self,
        question_id: Optional[int] = None,
        source: Optional[str] = None,
        concept: Optional[ConceptType] = None,
        process: Optional[ProcessType] = None,
    ) -> List[Question]:
        """Get questions from the database.

        Args:
            question_id (Optional[int], optional): The question id of the question. Defaults to None.
            source (Optional[str], optional): The source of the question. Defaults to None.
            concept (Optional[ConceptType], optional): The concept of questions. Defaults to None.
            process (Optional[ProcessType], optional): The process of questions. Defaults to None.

        Returns:
            List[Question]: The list of questions.
        """
        params = {}
        if question_id is not None:
            params["question_id"] = question_id
        if source is not None:
            params["source"] = source
        if concept is not None:
            params["concept"] = concept.value
        if process is not None:
            params["process"] = process.value

        response = await self.client.get(
            f"{self.base_url}/api/v1/bank/question/get", params=params
        )
        response.raise_for_status()
        return [Question.model_validate(q) for q in response.json()]

    async def approve_question(self, question_id: int) -> dict:
        """Approve a question in the database.

        Args:
            question_id (int): The id of the question.

        Returns:
            dict: The result of the operation.
        """
        data = {
            "question_id": question_id,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/bank/question/approve", json=data
        )
        response.raise_for_status()
        return response.json()

    async def delete_question(self, question_id: int) -> dict:
        """Delete a question in the database.

        Args:
            question_id (int): The id of the question.

        Returns:
            dict: The result of the operation.
        """
        response = await self.client.delete(
            f"{self.base_url}/api/v1/bank/question/delete",
            params={"question_id": question_id},
        )
        response.raise_for_status()
        return response.json()
