from typing import List
from httpx import Client, AsyncClient

from nanoko.models.user import Permission, User
from nanoko.models.assignment import (
    Class,
    FeedBack,
    Assignment,
)


class UserAPI:
    """The API for the user."""

    def __init__(self, base_url: str = "http://localhost:25324", client: Client = None):
        self.base_url = base_url
        self.client = client or Client()
        self._token = None

    def register(
        self,
        username: str,
        email: str,
        display_name: str,
        password: str,
        permission: Permission,
    ) -> User:
        """Register a new user.

        Args:
            username (str): Username for the new user.
            email (str): Email address for the new user.
            display_name (str): Display name for the new user.
            password (str): Password for the new user.
            permission (Permission): Permission level for the new user.

        Returns:
            User: The created user object.
        """
        data = {
            "username": username,
            "email": email,
            "display_name": display_name,
            "password": password,
            "permission": permission.value,
        }
        response = self.client.post(f"{self.base_url}/api/v1/user/register", json=data)
        response.raise_for_status()
        return User.model_validate(response.json())

    def login(self, username: str, password: str) -> None:
        """Login a user.

        Args:
            username (str): Username or email of the user.
            password (str): Password of the user.

        Returns:
            None: No return value.
        """
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "username": username,
            "password": password,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/user/token", headers=headers, data=data
        )
        response.raise_for_status()

        self._token = response.json()["access_token"]
        self.client.headers["Authorization"] = f"Bearer {self._token}"

        return None

    def me(self) -> User:
        """Get the current user's information.

        Returns:
            User: The current user's information.
        """
        response = self.client.get(f"{self.base_url}/api/v1/user/me")
        response.raise_for_status()
        return User.model_validate(response.json())

    def submit(self, sub_question_id: int, assignment_id: int, answer: str) -> FeedBack:
        """Submit an answer to a sub-question.

        Args:
            sub_question_id (int): The ID of the sub-question.
            assignment_id (int): The ID of the assignment.
            answer (str): The answer to the sub-question.

        Returns:
            FeedBack: The feedback on the submission.
        """
        data = {
            "sub_question_id": sub_question_id,
            "assignment_id": assignment_id,
            "answer": answer,
        }
        response = self.client.post(f"{self.base_url}/api/v1/user/submit", json=data)
        response.raise_for_status()
        return FeedBack.model_validate(response.json())

    def reset_password(self, old_password: str, new_password: str) -> dict:
        """Reset the password for the current user.

        Args:
            old_password (str): The current password of the user.
            new_password (str): The new password to set.

        Returns:
            dict: The result of the operation.
        """
        data = {"old_password": old_password, "new_password": new_password}
        response = self.client.post(
            f"{self.base_url}/api/v1/user/password/reset", json=data
        )
        response.raise_for_status()
        return response.json()

    def create_class(self, class_name: str, enter_code: str) -> Class:
        """Create a new class.

        Args:
            class_name (str): The name of the class.
            enter_code (str): The code to enter the class.

        Returns:
            Class: The created class object.
        """
        data = {"class_name": class_name, "enter_code": enter_code}
        response = self.client.post(
            f"{self.base_url}/api/v1/user/class/create", json=data
        )
        response.raise_for_status()
        return Class.model_validate(response.json())

    def join_class(self, class_name: str, enter_code: str) -> Class:
        """Join a class.

        Args:
            class_name (str): The name of the class.
            enter_code (str): The code to enter the class.

        Returns:
            Class: The joined class object.
        """
        data = {"class_name": class_name, "enter_code": enter_code}
        response = self.client.post(
            f"{self.base_url}/api/v1/user/class/join", json=data
        )
        response.raise_for_status()
        return Class.model_validate(response.json())

    def leave_class(self) -> dict:
        """Leave the current class.

        Returns:
            dict: The result of the operation.
        """
        response = self.client.post(f"{self.base_url}/api/v1/user/class/leave")
        response.raise_for_status()
        return response.json()

    def create_assignment(
        self,
        assignment_name: str,
        description: str,
        due_date: str,
        question_ids: List[int],
    ) -> Assignment:
        """Create a new assignment.

        Args:
            assignment_name (str): The name of the assignment.
            description (str): The description of the assignment.
            due_date (str): The due date of the assignment in ISO format.
            question_ids (List[int]): The list of question ids to include in the assignment.

        Returns:
            Assignment: The created assignment object.
        """
        data = {
            "assignment_name": assignment_name,
            "description": description,
            "due_date": due_date,
            "question_ids": question_ids,
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/user/assignment/create", json=data
        )
        response.raise_for_status()
        return Assignment.model_validate(response.json())

    def assign_assignment(self, assignment_id: int, class_id: int) -> dict:
        """Assign an assignment to a class.

        Args:
            assignment_id (int): The id of the assignment.
            class_id (int): The id of the class.

        Returns:
            dict: The result of the operation.
        """
        data = {"assignment_id": assignment_id, "class_id": class_id}
        response = self.client.post(
            f"{self.base_url}/api/v1/user/assignment/assign", json=data
        )
        response.raise_for_status()
        return response.json()

    def get_assignments(self) -> List[Assignment]:
        """Get all assignments for the current user.

        Returns:
            List[Assignment]: The list of assignments.
        """
        response = self.client.get(f"{self.base_url}/api/v1/user/assignments")
        response.raise_for_status()
        return [Assignment.model_validate(a) for a in response.json()]


class AsyncUserAPI:
    """The async API for the user."""

    def __init__(
        self, base_url: str = "http://localhost:25324", client: AsyncClient = None
    ):
        self.base_url = base_url
        self.client = client or AsyncClient()
        self._token = None

    async def register(
        self,
        username: str,
        email: str,
        display_name: str,
        password: str,
        permission: Permission,
    ) -> User:
        """Register a new user.

        Args:
            username (str): Username for the new user.
            email (str): Email address for the new user.
            display_name (str): Display name for the new user.
            password (str): Password for the new user.
            permission (Permission): Permission level for the new user.

        Returns:
            User: The created user object.
        """
        data = {
            "username": username,
            "email": email,
            "display_name": display_name,
            "password": password,
            "permission": permission.value,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/user/register", json=data
        )
        response.raise_for_status()
        return User.model_validate(response.json())

    async def login(self, username: str, password: str) -> None:
        """Login a user.

        Args:
            username (str): Username or email of the user.
            password (str): Password of the user.

        Returns:
            None: No return value.
        """
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "username": username,
            "password": password,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/user/token", headers=headers, data=data
        )
        response.raise_for_status()

        self._token = response.json()["access_token"]
        self.client.headers["Authorization"] = f"Bearer {self._token}"

        return None

    async def me(self) -> User:
        """Get the current user's information.

        Returns:
            User: The current user's information.
        """
        response = await self.client.get(f"{self.base_url}/api/v1/user/me")
        response.raise_for_status()
        return User.model_validate(response.json())

    async def submit(
        self, sub_question_id: int, assignment_id: int, answer: str
    ) -> FeedBack:
        """Submit an answer to a sub-question.

        Args:
            sub_question_id (int): The ID of the sub-question.
            assignment_id (int): The ID of the assignment.
            answer (str): The answer to the sub-question.

        Returns:
            FeedBack: The feedback on the submission.
        """
        data = {
            "sub_question_id": sub_question_id,
            "assignment_id": assignment_id,
            "answer": answer,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/user/submit", json=data
        )
        response.raise_for_status()
        return FeedBack.model_validate(response.json())

    async def reset_password(self, old_password: str, new_password: str) -> dict:
        """Reset the password for the current user.

        Args:
            old_password (str): The current password of the user.
            new_password (str): The new password to set.

        Returns:
            dict: The result of the operation.
        """
        data = {"old_password": old_password, "new_password": new_password}
        response = await self.client.post(
            f"{self.base_url}/api/v1/user/password/reset", json=data
        )
        response.raise_for_status()
        return response.json()

    async def create_class(self, class_name: str, enter_code: str) -> Class:
        """Create a new class.

        Args:
            class_name (str): The name of the class.
            enter_code (str): The code to enter the class.

        Returns:
            Class: The created class object.
        """
        data = {"class_name": class_name, "enter_code": enter_code}
        response = await self.client.post(
            f"{self.base_url}/api/v1/user/class/create", json=data
        )
        response.raise_for_status()
        return Class.model_validate(response.json())

    async def join_class(self, class_name: str, enter_code: str) -> Class:
        """Join a class.

        Args:
            class_name (str): The name of the class.
            enter_code (str): The code to enter the class.

        Returns:
            Class: The joined class object.
        """
        data = {"class_name": class_name, "enter_code": enter_code}
        response = await self.client.post(
            f"{self.base_url}/api/v1/user/class/join", json=data
        )
        response.raise_for_status()
        return Class.model_validate(response.json())

    async def leave_class(self) -> dict:
        """Leave the current class.

        Returns:
            dict: The result of the operation.
        """
        response = await self.client.post(f"{self.base_url}/api/v1/user/class/leave")
        response.raise_for_status()
        return response.json()

    async def create_assignment(
        self,
        assignment_name: str,
        description: str,
        due_date: str,
        question_ids: List[int],
    ) -> Assignment:
        """Create a new assignment.

        Args:
            assignment_name (str): The name of the assignment.
            description (str): The description of the assignment.
            due_date (str): The due date of the assignment in ISO format.
            question_ids (List[int]): The list of question ids to include in the assignment.

        Returns:
            Assignment: The created assignment object.
        """
        data = {
            "assignment_name": assignment_name,
            "description": description,
            "due_date": due_date,
            "question_ids": question_ids,
        }
        response = await self.client.post(
            f"{self.base_url}/api/v1/user/assignment/create", json=data
        )
        response.raise_for_status()
        return Assignment.model_validate(response.json())

    async def assign_assignment(self, assignment_id: int, class_id: int) -> dict:
        """Assign an assignment to a class.

        Args:
            assignment_id (int): The id of the assignment.
            class_id (int): The id of the class.

        Returns:
            dict: The result of the operation.
        """
        data = {"assignment_id": assignment_id, "class_id": class_id}
        response = await self.client.post(
            f"{self.base_url}/api/v1/user/assignment/assign", json=data
        )
        response.raise_for_status()
        return response.json()

    async def get_assignments(self) -> List[Assignment]:
        """Get all assignments for the current user.

        Returns:
            List[Assignment]: The list of assignments.
        """
        response = await self.client.get(f"{self.base_url}/api/v1/user/assignments")
        response.raise_for_status()
        return [Assignment.model_validate(a) for a in response.json()]
