from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class Performance(Enum):
    """A standard to represent the performance of students."""

    NOT_ACHIEVED = 0
    PARTIALLY_ACHIEVED = 1
    SATISFACTORILY_ACHIEVED = 2
    EXPERTLY_ACHIEVED = 3
    ADVANCED = 4


class Trend(Enum):
    """Trend used to indicate student performance trend over time."""

    SIGNIFICANT_DECLINE = -2
    DECLINE = -1
    STABLE = 0
    IMPROVEMENT = 1
    SIGNIFICANT_IMPROVEMENT = 2


class ProcessPerformances(BaseModel):
    """Performance of a student in process ideas."""

    formulate: float = Field(0, ge=0, le=4.0)
    apply: float = Field(0, ge=0, le=4.0)
    explain: float = Field(0, ge=0, le=4.0)


class Performances(BaseModel):
    """Performance of a student in all content ideas."""

    operations_on_numbers: ProcessPerformances
    mathematical_relationships: ProcessPerformances
    spatial_properties_and_representations: ProcessPerformances
    location_and_navigation: ProcessPerformances
    measurement: ProcessPerformances
    statistics_and_data: ProcessPerformances
    elements_of_chance: ProcessPerformances


class ProcessData(BaseModel):
    """Arrays of performances of a student in process ideas."""

    formulate: List[int] = []
    apply: List[int] = []
    explain: List[int] = []


class PerformancesData(BaseModel):
    """Arrays of performances of a student in all content ideas."""

    operations_on_numbers: ProcessData
    mathematical_relationships: ProcessData
    spatial_properties_and_representations: ProcessData
    location_and_navigation: ProcessData
    measurement: ProcessData
    statistics_and_data: ProcessData
    elements_of_chance: ProcessData


class ProcessTrends(BaseModel):
    """Trend of a student in process ideas."""

    formulate: Trend
    apply: Trend
    explain: Trend


class PerformanceTrends(BaseModel):
    """Trend of a student in all content ideas."""

    operations_on_numbers: ProcessTrends
    mathematical_relationships: ProcessTrends
    spatial_properties_and_representations: ProcessTrends
    location_and_navigation: ProcessTrends
    measurement: ProcessTrends
    statistics_and_data: ProcessTrends
    elements_of_chance: ProcessTrends
