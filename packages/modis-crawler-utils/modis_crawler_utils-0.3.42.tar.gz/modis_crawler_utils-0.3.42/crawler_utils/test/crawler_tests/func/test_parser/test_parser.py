import logging
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from pytest_cases import fixture
from pytest_check.context_manager import check
from pytest_dependency import depends

from crawler_utils.test.crawler_tests.exceptions import ReferenceDataError
from crawler_utils.test.crawler_tests.func.test_parser.check_parsers import (
    parsers_to_check,
)
from crawler_utils.test.crawler_tests.func.test_parser.parser_info import ParserInfo
from crawler_utils.test.crawler_tests.func.utils import (
    Item,
    filter_data,
    get_filtered_data,
    get_limit,
    iter_through_itemtype,
    parse_arguments,

)
from crawler_utils.test.crawler_tests.func.load_json import load_json_data
from crawler_utils.test.crawler_tests.func.settings  import DIR_TO_PROJECT

logger = logging.getLogger(__name__)


#  директории с эталонными данными
REFERENCE_ITEMS_DIR = DIR_TO_PROJECT / "reference_items"
MOCK_REFERENCE_DIR = REFERENCE_ITEMS_DIR / "mock_reference_items"
LIVE_REFERENCE_DIR = REFERENCE_ITEMS_DIR / "live_reference_items"



class LoadData:
    """
    Сlass to load cached (moc) data and data that has been saved as a result of a collection.

    Attributes:
        loaded_data (Dict[str, Any]): Stores result data loaded from specified paths.
        reference_data (Dict[str, Any]): Stores reference data (mock or live) loaded from
                                         predefined file paths based on the parser name.

    """

    def __init__(self):
        self.loaded_data: dict[str, Any] = {}
        self.reference_data: dict[str, Any] = {}

    def _get_reference_filename(self, parser_name: str, mock_mode: bool) -> Path:
        dirname = "mock_reference_items" if mock_mode else "live_reference_items"
        return Path(sys.path[-1]) / "reference_items" / dirname / f"get_{parser_name}_items.json"

    def load_reference_data(self, parser_info: str, mock_mode: bool) -> Any:
        if parser_info not in self.reference_data:
            self.reference_data[parser_info] = load_json_data(self._get_reference_filename(parser_info, mock_mode))
        return self.reference_data[parser_info]

    def load_result_data(self, parser_info: str, path_to_result_file: Path) -> Any:
        if parser_info not in self.loaded_data:
            self.loaded_data[parser_info] = load_json_data(path_to_result_file)
        return self.loaded_data[parser_info]


load_data = LoadData()


@fixture(scope="class", unpack_into="parser_info, itemtype")
@pytest.mark.parametrize(
    ("parser_info", "itemtype"), iter_through_itemtype(parsers_to_check), ids=lambda x: f"{x[0]!s}-{x[1]}"
)
def load_parser_data(parser_info: ParserInfo, itemtype: str, pytestconfig) -> Iterator[tuple[ParserInfo, str]]:
    mock_mode = pytestconfig.getoption("mock_mode")
    input_dir = pytestconfig.getoption("input_dir")
    args = parse_arguments()
    base_dir = MOCK_REFERENCE_DIR if args.save_items else Path(input_dir)
    path_to_result_file= base_dir / parser_info.path_to_test_results


    load_data.load_reference_data(str(parser_info), mock_mode)
    loaded_data = load_data.load_result_data(str(parser_info), path_to_result_file)

    expected_items_count = get_limit(str(parser_info), itemtype, mock_mode)
    reference_items_count = len(filter_data(loaded_data, itemtype))

    if expected_items_count and reference_items_count != expected_items_count:
        msg = f"Quantity of items in reference file ({reference_items_count}) doesn't match the limit value ({expected_items_count})."
        raise ReferenceDataError(
            msg
        )
    yield parser_info, itemtype


def get_name(parser_info: ParserInfo, itemtype: str) -> str:
    return f"TestParser::test_limit[{parser_info!s}-{itemtype}]"


class TestParser:
    """
    Класс тестов.

    механизм тестов:
        - для offline mock тестов:
              для каждого зарегестрированного парсера в файле check_parsers.py и
                  для каждого выводимого типа соответствующего парсера выполняются следующие тесты:

              1. test_limit: сравнивает количество сообщений типа itemtype полученного из кэша с референсными значениями
              2. test_value: сравнивает сообщения по элементно выкидывая url из attachmentа и timestamps

        - для online live тестов:
              схема точно такая же как и в случае mock тестов, однако
               1. все limit тесты пропускаются
               2. test_value проверяет наличие референсного контента в выдаче
                  (в mock режиме этот тест не падает только в случае полного сопадения кэша с референсом)
               3. в test_value item'ы сравниваются без учета unreliable fields (различных счетчиков, подверженных online изменениям)
    """

    tests_to_skip: list[str] = []

    @pytest.mark.dependency
    def test_limit(self, parser_info: ParserInfo, itemtype: str, pytestconfig):
        """Test that checks the number of items retrieved by the parser compared to the reference data."""
        mock_mode = pytestconfig.getoption("mock_mode")

        crawled_data, expected_data = get_filtered_data(
            load_data.loaded_data, load_data.reference_data, parser_info, itemtype
        )

        expected_items_count = len(expected_data)
        actual_items_count = len(crawled_data)

        if expected_items_count == actual_items_count == 0:
            TestParser.tests_to_skip.append(get_name(parser_info, itemtype))
            pytest.skip(
                f"Parser {parser_info.parser_name} returned an empty list of {itemtype}. All subsequent tests will be skipped."
            )

        if mock_mode:
            assert expected_items_count == actual_items_count, (
                f"Expected {expected_items_count} items, but got {actual_items_count}."
            )
        else:
            assert expected_items_count <= actual_items_count, (
                f"Expected at least {expected_items_count} items, but got {actual_items_count}."
            )

    def test_value(self, request: pytest.FixtureRequest, parser_info: ParserInfo, itemtype: str, pytestconfig):
        """Test that checks the contents of item type messages received by the parser against reference data."""
        mock_mode = pytestconfig.getoption("mock_mode")
        if mock_mode or get_name(parser_info, itemtype) in TestParser.tests_to_skip:
            depends(request, [get_name(parser_info, itemtype)])

        crawled_data, expected_data = get_filtered_data(
            load_data.loaded_data, load_data.reference_data, parser_info, itemtype
        )
        logger.info(f"Total number of messages: {len(expected_data)}")

        for expected_message in expected_data:
            expected_message = Item(expected_message)
            crawled_message = [Item(msg) for msg in crawled_data if Item(msg).id == expected_message.id]

            with check:
                assert crawled_message, f"Expected {expected_message}, but not found."
                assert len(crawled_message) == 1, f"Expected unique {expected_message}, but got {len(crawled_message)}."
                crawled_message = crawled_message[0]

                msg = (
                    f"Expected {expected_message}, but got {expected_message['type']}. See pytest verbose for details."
                )
                if mock_mode:
                    assert dict(crawled_message) == dict(expected_message), msg
                else:
                    assert crawled_message.filter() == expected_message.filter(), msg
