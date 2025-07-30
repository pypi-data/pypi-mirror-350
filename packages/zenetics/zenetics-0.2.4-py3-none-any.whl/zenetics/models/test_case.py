# from pydantic import BaseModel
from enum import Enum
from typing import Optional
from pydantic import Field

from zenetics.models.base import BaseSchema


class TestType(str, Enum):
    INTEGRATION = "integration"
    REFERENCE = "reference"


class TestCaseState(str, Enum):
    ACTIVE = "active"
    REVIEW = "review"
    OUTDATED = "outdated"
    DRAFT = "draft"


class TestCasePriority(str, Enum):
    MEDIUM = "medium"
    HIGH = "high"
    LOW = "low"
    CRITICAL = "critical"


class TestCaseData(BaseSchema):
    """Specification of the test case"""

    input: str = Field(..., min_length=1)
    input_context: Optional[str] = None
    reference_output: Optional[str] = None


class TestCase(BaseSchema):
    """Test case schema"""

    account_id: int
    application_id: int
    id: int
    version: int
    name: str
    description: str
    state: TestCaseState
    priority: TestCasePriority
    type: TestType
    data: TestCaseData
