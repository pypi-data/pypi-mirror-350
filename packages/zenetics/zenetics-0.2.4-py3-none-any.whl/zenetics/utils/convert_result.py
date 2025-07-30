from deepeval.metrics import BaseMetric
from zenetics.models.generation import TokenUsage
from zenetics.models.test_run import EvaluationResultState, EvaluatorResult


def convertResult(
    metric: BaseMetric, duration: float, tokens: TokenUsage
) -> EvaluatorResult:
    score = metric.score
    threshold = metric.threshold

    result = (
        EvaluationResultState.PASSED
        if score >= threshold
        else EvaluationResultState.FAILED
    )

    res = EvaluatorResult(
        threshold=threshold,
        score=score,
        reason=metric.reason,
        state=result,
        duration=duration,
        cost=metric.evaluation_cost,
        tokens=tokens,
        score_breakdown=metric.score_breakdown,
        verbose_logs=metric.verbose_logs,
    )
    return res
