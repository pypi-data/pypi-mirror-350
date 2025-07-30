from enum import Enum

from zenetics.models.base import BaseSchema


class TestSuiteState(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"


class TestSuite(BaseSchema):
    """Test suite schema"""

    id: int
    seq_id: int
    account_id: int
    application_id: int
    name: str
    description: str
    state: TestSuiteState
