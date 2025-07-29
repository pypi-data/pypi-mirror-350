from pydantic import BaseModel
from typing import Dict, Any
from ...base_models.chatty_asset_model import CompanyAssetModel
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import Field
import logging
logger = logging.getLogger("logger")

class FlowPreview(CompanyAssetModel):
    """This class is only used to preview the workflow. It is not used to create or update the flow."""
    title: str
    description: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))

    @classmethod
    def default_create_instance_method(cls, dict_data: Dict[str, Any]) -> 'FlowPreview':
        logger.info(f"Creating flow preview from dict: {dict_data}")
        return cls(created_at=dict_data.get("created_at", datetime.now(tz=ZoneInfo("UTC"))), updated_at=dict_data.get("updated_at", datetime.now(tz=ZoneInfo("UTC"))), **dict_data)