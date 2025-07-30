from enum import StrEnum
from pydantic import field_validator, ValidationInfo
from ....utils.types.identifier import StrObjectId
from typing import Optional, ClassVar
from ....utils.types.executor_types import ExecutorType
from ..base import Event, EventType, EventData
from ....company.empresa import EmpresaModel

class CompanyEventData(EventData):
    company_id: StrObjectId
    company : Optional[EmpresaModel] = None

    @property
    def message_group_id(self) -> str:
        return f"company-{self.company_id}"

class CompanyEvent(Event):
    data: CompanyEventData

    VALID_TYPES: ClassVar[set] = {
        EventType.COMPANY_CREATED,
        EventType.COMPANY_UPDATED,
        EventType.COMPANY_DELETED
    }

    @field_validator('data')
    def validate_data_fields(cls, v: CompanyEventData, info: ValidationInfo):
        if info.data.get('type') == EventType.COMPANY_CREATED and not v.company:
            raise ValueError("company must be set for COMPANY_CREATED events")
        if info.data.get('type') == EventType.COMPANY_UPDATED and not v.company:
            raise ValueError("company must be set for COMPANY_UPDATED events")
        return v
