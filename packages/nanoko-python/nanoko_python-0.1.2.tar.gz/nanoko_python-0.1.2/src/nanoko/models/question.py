from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class ConceptType(Enum):
    """Concept enum for the concept of subquestions."""

    OPERATIONS_ON_NUMBERS = 0
    MATHEMATICAL_RELATIONSHIPS = 1
    SPATIAL_PROPERTIES_AND_REPRESENTATIONS = 2
    LOCATION_AND_NAVIGATION = 3
    MEASUREMENT = 4
    STATISTICS_AND_DATA = 5
    ELEMENTS_OF_CHANCE = 6


class ProcessType(Enum):
    """Process enum for the process of subquestions."""

    FORMULATE = 0
    APPLY = 1
    EXPLAIN = 2


class SubQuestion(BaseModel):
    """API model for subquestion."""

    id: Optional[int] = None
    description: str
    answer: str
    concept: ConceptType
    process: ProcessType
    keywords: Optional[List[str]] = None
    options: Optional[List[str]] = None
    image_id: Optional[int] = None


class Question(BaseModel):
    """API model for question."""

    id: Optional[int] = None
    source: str
    is_audited: Optional[bool] = None
    is_deleted: Optional[bool] = None
    sub_questions: List[SubQuestion]
