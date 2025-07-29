from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from typing import ClassVar
from ....utils.types.identifier import StrObjectId
from ....company.assets.product import Product
from typing import Optional
from pydantic import field_validator, ValidationInfo, Field
class ProductChatData(CustomerEventData):
    product_id: StrObjectId
    product: Optional[Product] = Field(description="The product object")
    time_to_product_seconds: Optional[int] = None

class ProductChatEvent(Event):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    data: ProductChatData

    VALID_TYPES: ClassVar[set] = {
        EventType.PRODUCT_ASSIGNED,
        EventType.PRODUCT_REMOVED
    }

    @field_validator('data')
    def validate_data_fields(cls, v: ProductChatData, info: ValidationInfo):
        if info.data.get('type') != EventType.PRODUCT_REMOVED and not v.product:
            raise ValueError("product must be set for all events except PRODUCT_REMOVED")
        return v

