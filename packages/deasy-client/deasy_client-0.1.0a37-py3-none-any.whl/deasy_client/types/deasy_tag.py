# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DeasyTag"]


class DeasyTag(BaseModel):
    created_at: datetime

    description: str

    name: str

    tag_id: str

    username: str

    available_values: Optional[List[str]] = None

    date_format: Optional[str] = None

    examples: Optional[List[Union[Dict[str, object], str]]] = None

    max_values: Optional[int] = FieldInfo(alias="maxValues", default=None)

    output_type: Optional[str] = None

    tuned: Optional[int] = None

    updated_at: Optional[datetime] = None
