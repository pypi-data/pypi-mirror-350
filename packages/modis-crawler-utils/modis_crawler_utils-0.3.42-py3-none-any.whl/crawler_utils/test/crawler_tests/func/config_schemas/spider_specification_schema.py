from collections.abc import Mapping
from pathlib import Path
from typing import Literal
from typing import Union

from pydantic import BaseModel, field_validator

AllowedItemTypes = Literal[
    "user_profile",
    "group_profile",
    "message",
    "post",
    "comment",
    "video",
    "photo",
    "audio",
    "news",
    "social_connection",
    "follower",
    "friend",
    "admin",
    "reaction",
]

AllowedReturnModels = Literal[
    "UserProfile",
    "GroupProfile",
    "Message",
    "SocialConnection",
]


class Parser(BaseModel):
    parser_name: str
    path_to_test_results: str
    output_itemtypes: list[AllowedReturnModels]

    @field_validator("path_to_test_results")
    def validate_json_path(cls, value: str) -> str: 
        path = Path(value)
        if path.suffix.lower() != ".json":
            raise ValueError(f"Path '{value}' is not a JSON file")
        return str(path)



class SpiderNames(BaseModel):
    search: str
    target: str


class Spiders(BaseModel):
    parsers: list[Parser]
    spider_names: SpiderNames


class SpidersSpecificationSchema(BaseModel):
    spiders: Spiders
    limits2type: Mapping[str, Union[AllowedItemTypes, list[AllowedItemTypes]]] | None

