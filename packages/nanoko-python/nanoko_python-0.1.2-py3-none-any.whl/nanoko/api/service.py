from typing import Optional
from datetime import datetime
from httpx import Client, AsyncClient

from nanoko.models.performance import (
    Performances,
    PerformancesData,
    PerformanceTrends,
)


class ServiceAPI:
    """The API for the service."""

    def __init__(self, base_url: str = "http://localhost:25324", client: Client = None):
        self.base_url = base_url
        self.client = client or Client()

    def get_performances(self, user_id: int) -> PerformancesData:
        """Get the performance of a user.

        Args:
            user_id (int): The id of the user to get the performance for.

        Returns:
            PerformancesData: The performance data of the user.
        """
        params = {"user_id": user_id}
        response = self.client.get(
            f"{self.base_url}/api/v1/service/performances", params=params
        )
        response.raise_for_status()
        return PerformancesData.model_validate(response.json())

    def get_best_performances(self, user_id: int) -> Performances:
        """Get the best performance of a user.

        Args:
            user_id (int): The id of the user to get the performance for.

        Returns:
            Performances: The best performance data of the user.
        """
        params = {"user_id": user_id}
        response = self.client.get(
            f"{self.base_url}/api/v1/service/performances/best", params=params
        )
        response.raise_for_status()
        return Performances.model_validate(response.json())

    def get_average_performances(self, user_id: int) -> Performances:
        """Get the average performance of a user.

        Args:
            user_id (int): The id of the user to get the performance for.

        Returns:
            Performances: The average performance data of the user.
        """
        params = {"user_id": user_id}
        response = self.client.get(
            f"{self.base_url}/api/v1/service/performances/average", params=params
        )
        response.raise_for_status()
        return Performances.model_validate(response.json())

    def get_recent_best_performances(
        self, user_id: int, start_time: datetime
    ) -> Performances:
        """Get the recent best performance of a user.

        Args:
            user_id (int): The id of the user to get the performance for.
            start_time (datetime): The start time to get the performance from.

        Returns:
            Performances: The recent best performance data of the user.
        """
        params = {"user_id": user_id, "start_time": start_time.isoformat()}
        response = self.client.get(
            f"{self.base_url}/api/v1/service/performances/best/recent", params=params
        )
        response.raise_for_status()
        return Performances.model_validate(response.json())

    def get_recent_average_performances(
        self, user_id: int, start_time: datetime
    ) -> Performances:
        """Get the recent average performance of a user.

        Args:
            user_id (int): The id of the user to get the performance for.
            start_time (datetime): The start time to get the performance from.

        Returns:
            Performances: The recent average performance data of the user.
        """
        params = {"user_id": user_id, "start_time": start_time.isoformat()}
        response = self.client.get(
            f"{self.base_url}/api/v1/service/performances/average/recent", params=params
        )
        response.raise_for_status()
        return Performances.model_validate(response.json())

    def get_performance_trends(
        self, user_id: int, start_time: Optional[datetime] = None
    ) -> PerformanceTrends:
        """Get the performance trends of a user.

        Args:
            user_id (int): The id of the user to get the performance trends for.
            start_time (Optional[datetime], optional): The start time to get the performance trends from. Defaults to None.

        Returns:
            PerformanceTrends: The performance trends data of the user.
        """
        params = {"user_id": user_id}
        if start_time is not None:
            params["start_time"] = start_time.isoformat()
        response = self.client.get(
            f"{self.base_url}/api/v1/service/performances/trends", params=params
        )
        response.raise_for_status()
        return PerformanceTrends.model_validate(response.json())


class AsyncServiceAPI:
    """The async API for the service."""

    def __init__(
        self, base_url: str = "http://localhost:25324", client: AsyncClient = None
    ):
        self.base_url = base_url
        self.client = client or AsyncClient()

    async def get_performances(self, user_id: int) -> PerformancesData:
        """Get the performance of a user.

        Args:
            user_id (int): The id of the user to get the performance for.

        Returns:
            PerformancesData: The performance data of the user.
        """
        params = {"user_id": user_id}
        response = await self.client.get(
            f"{self.base_url}/api/v1/service/performances", params=params
        )
        response.raise_for_status()
        return PerformancesData.model_validate(response.json())

    async def get_best_performances(self, user_id: int) -> Performances:
        """Get the best performance of a user.

        Args:
            user_id (int): The id of the user to get the performance for.

        Returns:
            Performances: The best performance data of the user.
        """
        params = {"user_id": user_id}
        response = await self.client.get(
            f"{self.base_url}/api/v1/service/performances/best", params=params
        )
        response.raise_for_status()
        return Performances.model_validate(response.json())

    async def get_average_performances(self, user_id: int) -> Performances:
        """Get the average performance of a user.

        Args:
            user_id (int): The id of the user to get the performance for.

        Returns:
            Performances: The average performance data of the user.
        """
        params = {"user_id": user_id}
        response = await self.client.get(
            f"{self.base_url}/api/v1/service/performances/average", params=params
        )
        response.raise_for_status()
        return Performances.model_validate(response.json())

    async def get_recent_best_performances(
        self, user_id: int, start_time: datetime
    ) -> Performances:
        """Get the recent best performance of a user.

        Args:
            user_id (int): The id of the user to get the performance for.
            start_time (datetime): The start time to get the performance from.

        Returns:
            Performances: The recent best performance data of the user.
        """
        params = {"user_id": user_id, "start_time": start_time.isoformat()}
        response = await self.client.get(
            f"{self.base_url}/api/v1/service/performances/best/recent", params=params
        )
        response.raise_for_status()
        return Performances.model_validate(response.json())

    async def get_recent_average_performances(
        self, user_id: int, start_time: datetime
    ) -> Performances:
        """Get the recent average performance of a user.

        Args:
            user_id (int): The id of the user to get the performance for.
            start_time (datetime): The start time to get the performance from.

        Returns:
            Performances: The recent average performance data of the user.
        """
        params = {"user_id": user_id, "start_time": start_time.isoformat()}
        response = await self.client.get(
            f"{self.base_url}/api/v1/service/performances/average/recent", params=params
        )
        response.raise_for_status()
        return Performances.model_validate(response.json())

    async def get_performance_trends(
        self, user_id: int, start_time: Optional[datetime] = None
    ) -> PerformanceTrends:
        """Get the performance trends of a user.

        Args:
            user_id (int): The id of the user to get the performance trends for.
            start_time (Optional[datetime], optional): The start time to get the performance trends from. Defaults to None.

        Returns:
            PerformanceTrends: The performance trends data of the user.
        """
        params = {"user_id": user_id}
        if start_time is not None:
            params["start_time"] = start_time.isoformat()
        response = await self.client.get(
            f"{self.base_url}/api/v1/service/performances/trends", params=params
        )
        response.raise_for_status()
        return PerformanceTrends.model_validate(response.json())
