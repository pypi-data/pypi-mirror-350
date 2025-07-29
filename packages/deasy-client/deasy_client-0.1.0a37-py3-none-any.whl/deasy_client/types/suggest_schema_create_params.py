# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["SuggestSchemaCreateParams", "Node"]


class SuggestSchemaCreateParams(TypedDict, total=False):
    data_connector_name: Required[str]

    auto_save: Optional[bool]

    condition: Optional["ConditionInputParam"]

    context_level: Optional[str]

    current_tree: Optional[Dict[str, object]]

    dataslice_id: Optional[str]

    file_names: Optional[List[str]]

    graph_tag_type: Optional[Literal["open_ended", "binary", "mixed", "defined_values"]]

    llm_profile_name: Optional[str]

    max_height: Optional[int]

    max_tags_per_level: Optional[int]

    min_tags_per_level: Optional[int]

    node: Optional[Node]

    progress_tracking_id: Optional[str]

    schema_name: Optional[str]

    set_max_values: Optional[bool]

    suggestion_root: Optional[Literal["root", "document_type"]]

    use_existing_tags: Optional[bool]

    use_extracted_tags: Optional[bool]

    use_mix_llm_and_source: Optional[bool]

    user_context: Optional[str]

    values_per_tag: Optional[int]


class Node(TypedDict, total=False):
    label: Optional[str]

    path: Optional[List[str]]


from .condition_input_param import ConditionInputParam
