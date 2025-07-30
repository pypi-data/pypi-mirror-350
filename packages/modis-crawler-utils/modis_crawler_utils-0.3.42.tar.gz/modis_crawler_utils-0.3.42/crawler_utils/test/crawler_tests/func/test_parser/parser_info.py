
from pydantic_core import PydanticUndefined

from crawler_utils.social_media.items import (
    GroupProfile,
    Message,
    MessageType,
    SocialConnection,
    SocialMediaItem,
    UserProfile,
)


class ParserInfo:
    """
    Class for storing and managing information about the parser, including its name, path to test results,
    and the types of social media items it produces.

    Attributes:
        parser_name (str): Name of the parser.
        path_to_test_results (str): Path to the directory where test results are stored.
        _output_itemtypes (set[Type[SocialMediaItem]]): Set of output item types associated with this parser.

    """

    _possible_itemtypes: tuple[type[SocialMediaItem], ...] = (UserProfile, GroupProfile, Message, SocialConnection)

    parser_name: str
    path_to_test_results: str
    _output_itemtypes: set[type[SocialMediaItem]] = set()

    def __init__(self, parser_name: str, path_to_test_results: str, output_itemtypes: list[str]):
        self.parser_name = parser_name
        self.path_to_test_results = path_to_test_results

        possible_itemtype_names = (itemtype.__name__ for itemtype in self._possible_itemtypes)
        itemtype_mapping = dict(zip(possible_itemtype_names, self._possible_itemtypes, strict=False))
        self._output_itemtypes = {itemtype_mapping[itemtype] for itemtype in output_itemtypes}

    def __str__(self):
        return self.parser_name

    @property
    def output_itemtypes(self) -> list[str | None]:
        default_itemtypes = [itemtype.model_fields["type"].default for itemtype in self._output_itemtypes]

        if "message" in default_itemtypes:
            default_itemtypes.remove("message")
            default_itemtypes += [e.name.lower() for e in MessageType]
        return [item for item in default_itemtypes if item is not PydanticUndefined]

    def get_itemtype_cls(self, itemtype_name: str) -> type[SocialMediaItem]:
        for itemtype, cls in zip(self.output_itemtypes, self._output_itemtypes, strict=False):
            if itemtype == itemtype_name:
                return cls
        msg = f"Item type '{itemtype_name}' not found."
        raise ValueError(msg)
