from typing import Optional

from zenetics.models.base import BaseSchema


class Evaluator(BaseSchema):
    """Shared evaluator properties"""

    id: int
    name: str
    description: Optional[str]
    type: str
    category: str
    defaultThreshold: float


class EvaluatorAssignment(BaseSchema):
    account_id: int
    application_id: int
    evaluator_id: int
    test_suite_id: int
    id: int
    evaluator: Evaluator
    threshold: float
    config: dict
