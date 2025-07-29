from zsynctech_maestro_sdk.errors.exceptions import InvalidIDFormatException, InvalidDateFormatException
from zsynctech_maestro_sdk.utils import get_current_time_iso
from pydantic import BaseModel, field_validator, Field
from uuid_extensions import uuid7
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid
import re


class ExecutionStatus(str, Enum):
    WAITING = 'WAITING'
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'
    ERROR = 'ERROR'
    SCHEDULED = 'SCHEDULED'
    INTERRUPTED = 'INTERRUPTED'


class ExecutionModel(BaseModel):
    id: str = Field(
        default_factory=lambda: uuid7().hex
    )
    observation: Optional[str] = None
    status: Optional[ExecutionStatus] = ExecutionStatus.WAITING
    endDate: Optional[str] = None
    totalTaskCount: Optional[int] = 0
    currentTaskCount: Optional[int] = 0

    @classmethod
    def validate_uuid_version(cls, value):
        try:
            uuid_obj = uuid.UUID(value)
        except:
            raise InvalidIDFormatException(
                "Invalid ID format. Expected a UUIDv7 string. Use uuid_extensions.uuid7() to generate a valid UUIDv7 string."
            )

        if not uuid_obj.version == 7:
            raise InvalidIDFormatException(
                "Invalid ID format. Expected a UUIDv7 string. Use uuid_extensions.uuid7() to generate a valid UUIDv7 string."
            )

    def __setattr__(self, name, value):

        if name == 'currentTaskCount' or name == 'totalTaskCount':
            if isinstance(value, int) and value < 0:
                raise ValueError("currentTaskCount and totalTaskCount must be non-negative integers.")

        if name == 'id':
            self.validate_uuid_version(value)
        if name == 'endDate':
            self.validate_end_date(value)
        if name == 'status':
            if value in [ExecutionStatus.ERROR, ExecutionStatus.FINISHED, ExecutionStatus.INTERRUPTED]:
                super().__setattr__('endDate', get_current_time_iso())
            else:
                super().__setattr__('endDate', None)
    
        super().__setattr__(name, value)


    @field_validator('endDate', mode='before')
    def validate_end_date(cls, value):
        if value is None:
            return value

        iso_format_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$'
        if not re.match(iso_format_regex, value):
            raise InvalidDateFormatException("Invalid endDate format. Expected format: YYYY-MM-DDTHH:MM:SS.sssZ")

        try:
            datetime.strptime(value[:-1], '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            raise InvalidDateFormatException("Invalid endDate value. Date does not represent a valid date.")

        return value

