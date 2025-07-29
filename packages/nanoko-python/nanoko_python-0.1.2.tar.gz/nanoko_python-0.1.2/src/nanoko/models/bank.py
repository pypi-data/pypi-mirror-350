from typing import List

from nanoko.models.question import ConceptType, ProcessType


class ImageAddRequest:
    """API model for image addition request."""

    def __init__(self, description: str, hash: str):
        self.description = description
        self.hash = hash


class ImageDescriptionRequest:
    """API model for image description request."""

    def __init__(self, image_id: int, description: str):
        self.image_id = image_id
        self.description = description


class ImageHashRequest:
    """API model for image hash request."""

    def __init__(self, image_id: int, hash: str):
        self.image_id = image_id
        self.hash = hash


class SubQuestionDescriptionRequest:
    """API model for sub-question description request."""

    def __init__(self, sub_question_id: int, description: str):
        self.sub_question_id = sub_question_id
        self.description = description


class SubQuestionOptionsRequest:
    """API model for sub-question options request."""

    def __init__(self, sub_question_id: int, options: List[str]):
        self.sub_question_id = sub_question_id
        self.options = options


class SubQuestionAnswerRequest:
    """API model for sub-question answer request."""

    def __init__(self, sub_question_id: int, answer: str):
        self.sub_question_id = sub_question_id
        self.answer = answer


class SubQuestionConceptRequest:
    """API model for sub-question concept request."""

    def __init__(self, sub_question_id: int, concept: ConceptType):
        self.sub_question_id = sub_question_id
        self.concept = concept


class SubQuestionProcessRequest:
    """API model for sub-question process request."""

    def __init__(self, sub_question_id: int, process: ProcessType):
        self.sub_question_id = sub_question_id
        self.process = process


class SubQuestionKeywordsRequest:
    """API model for sub-question keywords request."""

    def __init__(self, sub_question_id: int, keywords: List[str]):
        self.sub_question_id = sub_question_id
        self.keywords = keywords


class SubQuestionImageRequest:
    """API model for sub-question image request."""

    def __init__(self, sub_question_id: int, image_id: int):
        self.sub_question_id = sub_question_id
        self.image_id = image_id


class QuestionApproveRequest:
    """API model for question approval request."""

    def __init__(self, question_id: int):
        self.question_id = question_id
