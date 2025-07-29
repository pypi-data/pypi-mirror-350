from zsynctech_maestro_sdk.utils import get_current_time_iso
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from uuid_extensions import uuid7
from datetime import datetime
from enum import Enum
import uuid
import re


class StepStatus(str, Enum):
    UNPROCESSED = 'UNPROCESSED'
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'


class StepModel(BaseModel):
    id: str = Field(
        default_factory=lambda: uuid7().hex
    )
    observation: Optional[str] = None
    operation: Optional[Literal["create", "update"]] = None
    taskId: Optional[str] = None
    automationOnClientId: Optional[str] = None
    status: Optional[StepStatus] = StepStatus.UNPROCESSED
    step: Optional[str] = None
    endDate: Optional[str] = None

    @classmethod
    def validate_uuid_version(cls, value):

        if not isinstance(value, str):
            raise ValueError(
                "Invalid ID format. Expected a UUIDv7 string. Use uuid_extensions.uuid7() to generate a valid UUIDv7 string."
            )

        try:
            uuid_obj = uuid.UUID(value)
        except:
            raise ValueError(
                "Invalid ID format. Expected a UUIDv7 string. Use uuid_extensions.uuid7() to generate a valid UUIDv7 string."
            )

        if not uuid_obj.version == 7:
            raise ValueError(
                "Invalid ID format. Expected a UUIDv7 string. Use uuid_extensions.uuid7() to generate a valid UUIDv7 string."
            )

    def __setattr__(self, name, value):
        if name == 'id':
            self.validate_uuid_version(value)
        if name == 'operation':
            self.validate_operation(value)
        if name == 'endDate':
            self.validate_end_date(value)
        if name == 'status':
            if value in [StepStatus.FAIL, StepStatus.SUCCESS]:
                super().__setattr__('endDate', get_current_time_iso())
            else:
                super().__setattr__('endDate', None)
        super().__setattr__(name, value)

    @field_validator('operation', mode='before')
    def validate_operation(cls, value):
        if value not in ["create", "update"]:
            raise ValueError("Invalid operation. Must be 'create' or 'update'.")
        return value
    
    @field_validator('id', mode='before')
    def validate_id(cls, value):
        cls.validate_uuid_version(value)
        return value

    @field_validator('endDate', mode='before')
    def validate_end_date(cls, value):
        if value is None:
            return value

        iso_format_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$'
        if not re.match(iso_format_regex, value):
            raise ValueError("Invalid endDate format. Expected format: YYYY-MM-DDTHH:MM:SS.sssZ")

        try:
            datetime.strptime(value[:-1], '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            raise ValueError("Invalid endDate value. Date does not represent a valid date.")

        return value
