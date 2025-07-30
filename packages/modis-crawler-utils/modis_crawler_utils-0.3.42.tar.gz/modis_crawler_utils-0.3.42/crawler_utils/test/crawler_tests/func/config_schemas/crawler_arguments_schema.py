from collections.abc import Mapping

from pydantic import BaseModel


class CrawlerArgumentsSchema(BaseModel):
    ARGUMENTS_FOR_LIVE_TESTS: Mapping[str, list[list[str]]]
    ARGUMENTS_FOR_MOCK_TESTS: Mapping[str, list[list[str]]]
