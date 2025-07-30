from typing import List, Any

from pydantic import BaseModel, Field

from zenetics.models.evaluator import EvaluatorAssignment
from zenetics.models.generation import Generation
from zenetics.models.test_case import TestCase


class EvaluatorBatchElement(BaseModel):
    """
    Data class for holding test case, generated output, and evaluator for
    batch evaluations.

    This class is used to group all the elements needed for a single
    evaluation.
    """

    test_case: TestCase
    generated_output: Generation
    evaluator: EvaluatorAssignment


class EvaluatorBatch(BaseModel):
    """
    Data class for holding a batch of evaluation elements.

    This class is used to group multiple evaluation elements for batch
    processing.
    """

    elements: List[EvaluatorBatchElement]


class EvaluatorBatchResult(BaseModel):
    """
    Data class for holding the results of a batch evaluation.

    Each result can be either an EvaluatorResult or an Exception
    if the evaluation failed.
    """

    # Use Any type here instead of Union[EvaluatorResult, Exception]
    # to avoid Pydantic schema generation issues
    results: List[Any] = Field(
        description="Results of batch evaluation. Can be EvaluatorResult "
        "objects or Exceptions"
    )

    model_config = {"arbitrary_types_allowed": True}

    @property
    def success_count(self) -> int:
        """Count the number of successful evaluations."""
        return sum(1 for result in self.results if not isinstance(result, Exception))

    @property
    def failure_count(self) -> int:
        """Count the number of failed evaluations."""
        return sum(1 for result in self.results if isinstance(result, Exception))

    @property
    def success_rate(self) -> float:
        """Calculate the success rate as a percentage."""
        if not self.results:
            return 0.0
        return (self.success_count / len(self.results)) * 100.0
