from ...base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from pydantic import Field
from typing import Optional, Any, ClassVar
from pydantic import BaseModel
from ...utils.types import StrObjectId

class TagPreview(ChattyAssetPreview):
    color: str

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"color": 1}

class Tag(CompanyAssetModel):
    name: str
    description: str
    color: str
    is_event: bool
    event_name: Optional[str] = Field(default=None)
    preview_class: ClassVar[type[TagPreview]] = TagPreview

