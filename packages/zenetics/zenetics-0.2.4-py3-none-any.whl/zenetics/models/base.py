from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration"""

    model_config = ConfigDict(
        from_attributes=True,  # Allow ORM model parsing
        populate_by_name=True,  # Allow population by alias
        alias_generator=lambda x: "".join(
            word.capitalize() if i else word for i, word in enumerate(x.split("_"))
        ),  # camelCase
        json_encoders={datetime: lambda v: v.isoformat()},
        serialize_by_alias=True,  # Always use camelCase in JSON output
        arbitrary_types_allowed=True,
    )

    # Override the model_dump_json method to ensure camelCase
    def model_dump_json(self, **kwargs):
        kwargs.setdefault("by_alias", True)
        return super().model_dump_json(**kwargs)

    # Override the model_dump method as well
    def model_dump(self, **kwargs):
        kwargs.setdefault("by_alias", True)
        return super().model_dump(**kwargs)


class TimestampedSchema(BaseSchema):
    """Base schema including timestamp fields"""

    created_at: datetime
    updated_at: datetime
