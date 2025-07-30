from __future__ import annotations

import argparse
import copy
import itertools
import logging
import sys
import time
from collections import UserDict
from pathlib import Path
from typing import TYPE_CHECKING

from scrapy.utils.misc import walk_modules
from scrapy.utils.spider import iter_spider_classes

from crawler_utils.test.crawler_tests.exceptions import LimitNotRegistred, MultipleTestingArgumentsNotSupported
from crawler_utils.test.crawler_tests.func.settings import SPIDER_NAMES, arguments_data, spiders_specification

if TYPE_CHECKING:
    from scrapy.spiders import Spider

ARGUMENTS_FOR_MOCK_TESTS = arguments_data.get("ARGUMENTS_FOR_MOCK_TESTS", {})
ARGUMENTS_FOR_LIVE_TESTS = arguments_data.get("ARGUMENTS_FOR_LIVE_TESTS", {})


class Item(UserDict):
    """
    Класс обертка для сообщений сборщика.
    Инкапсулирует логику сравнения сообщений в контексте их полей, с учетом типа сообщения.

    Item.id - играет роль uuid'а сообщения в рамках одного сбора. Используется для сравнения двух item'ов

    Полное сравнение:
    обычное поэлементрое сравнение словарей: dict(item1) == dict(item2)
    используется для offline mock-тестов, для полной проверки работоспособности модулей

    сравнение отфильтрованых значений item1.filter() == item2.filter(). сравниваются только reliable поля (без
    реакций, количества просмотров и прочих unreliable полей, которые часто подвержены изменениям)
    """

    # поля которые уникально идентифицируют сообщения в рамках одного сбора
    itemtype2id = {"comment": ["message_id"], "social_connection": ["from_id", "to_id"]}

    # поля которые довольно часто меняются
    unreliable_field_suffuxes = ["_count", "last_logged_in"]

    def __init__(self, dict):
        super().__init__(dict)
        self.data = Item._remove_timedependent_fields(self.data)

    def __str__(self) -> str:
        prefix = "social_connection " if self["type"] == "social_connection" else f"{self['type']} with "
        return prefix + ", ".join([f"{key}: {val}" for key, val in self.id.items()])

    def __repr__(self) -> str:
        return f"Item({self.id}, type={self['type']})"

    @property
    def id(self) -> dict:
        return {_id: self[_id] for _id in self.itemtype2id.get(self["type"], ["url"])}

    def filter(self) -> dict:
        # фильтр по частоменяющимся полям
        dict_to_return = Item(copy.deepcopy(dict(self)))
        for suffix in self.unreliable_field_suffuxes:
            fields_to_pop = list(filter(lambda field: suffix in field, dict_to_return.keys()))
            for field_to_pop in fields_to_pop:
                dict_to_return.pop(field_to_pop)
        return dict(dict_to_return)

    @classmethod
    def _remove_timedependent_fields(cls, data):
        data.pop("_timestamp", None)
        for attachment in data.get("_attachments", []):
            attachment.pop("url", None)
        for value in data.values():
            if isinstance(value, dict):
                value = cls._remove_timedependent_fields(value)
            if isinstance(value, list):
                value = [cls._remove_timedependent_fields(el) if isinstance(el, dict) else el for el in value]
        return data


def get_spiders(spider_dir, spider_names) -> dict[str, Spider]:
    ret_spiders = {}
    for module in walk_modules(spider_dir):
        for spider in iter_spider_classes(module):
            if spider.name in spider_names:
                ret_spiders[spider.name] = spider
    return ret_spiders


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время выполнения функции {func.__name__}: {execution_time:.4f} секунд")
        return result

    return wrapper


def filter_data(data, itemtype):
    return [item for item in data if item.get("type") == itemtype]


def iter_through_itemtype(parsers_to_check):
    return itertools.chain.from_iterable(itertools.product([x], x.output_itemtypes) for x in parsers_to_check)


def get_filtered_data(loaded_data, reference_data, parser_info, itemtype):
    crawled_data = loaded_data[str(parser_info)]
    expected_data = reference_data[str(parser_info)]
    crawled_data = filter_data(crawled_data, itemtype)
    expected_data = filter_data(expected_data, itemtype)
    return crawled_data, expected_data


def get_limit(parser_name: str, itemtype: str, mock_mode: bool) -> int | None:
    limits2type = spiders_specification.get("limits2type", {})

    def choose_by_itemtype(arg):
        limit_type, *_ = arg.split("_result_limit")
        try:
            return limits2type[limit_type] == itemtype
        except KeyError as key:
            filepath = Path(__file__).relative_to(Path.cwd())
            msg = f"Argument {key}_result_limit are not registered in get_limit. Check {filepath}"
            raise LimitNotRegistred(msg)

    def filter_limit_args(arg_string):
        return filter(lambda arg: "limit" in arg, arg_string)

    def flatten_list(nested_list):
        return [el for nested_el in nested_list for el in nested_el]

    parser_args = get_arg_by_parser_name(parser_name, mock_mode)
    parser_limit_args = flatten_list(map(filter_limit_args, parser_args))  # filter only limits args
    filtered_parser_limit_args = list(
        filter(choose_by_itemtype, parser_limit_args)
    )  # filter only limit args with out specific parser's ooutput type

    if not filtered_parser_limit_args:
        return None

    limit_arg_name, limit_arg_value, *_ = filtered_parser_limit_args[0].split("=")

    return int(limit_arg_value)


def get_arg_by_parser_name(parser_name: str, mock_mode: bool) -> list[list[str]]:
    def choose_by_parser_name(args: dict):
        return parser_name in args[1]

    arguments = ARGUMENTS_FOR_MOCK_TESTS if mock_mode else ARGUMENTS_FOR_LIVE_TESTS
    arg_dict = arguments[SPIDER_NAMES["search"]] if "search" in parser_name else arguments[SPIDER_NAMES["target"]]
    parser_args = [args for args in arg_dict if choose_by_parser_name(args)]

    if len(parser_args) > 1:
        raise MultipleTestingArgumentsNotSupported

    return parser_args[0]


def get_args_by_parser_names(pytest_k_args: list[str], mock_mode):
    args = []
    for pytest_k_arg in pytest_k_args:
        parser_name, *_ = pytest_k_arg.split("-")
        args += get_arg_by_parser_name(parser_name, mock_mode)
    return args


def get_args(mock_mode, create_test_data):
    args = []
    arg_dict = ARGUMENTS_FOR_MOCK_TESTS if mock_mode or create_test_data else ARGUMENTS_FOR_LIVE_TESTS
    for spider_args in arg_dict.values():
        args += spider_args
    return args


def setup_logger():
    logger = logging.getLogger(__name__)

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parser args for tests")

    parser.add_argument("--mock-mode", action="store_true", help="Enable mock mode")
    parser.add_argument("--save-items", action="store_true", help="Save  crawled items from tmp dir")
    parser.add_argument(
        "--output-items-dir",
        action="store",
        default="./saved_items",
        help="Directory for saving crawled temporary files. Default: current working directory will be used.",
    )
    parser.add_argument(
        "--input-dir", action="store", type=str, help="Directory for input files."
    )  # TODO надо будет заменить этот флаг на  --output-items-dir
    parser.add_argument("-f", dest="parser_names", action="append", default=None, help="Filter by parser name.")
    parser.add_argument("--create-test-data", action="store_true", help="Update crawled items to cache")
    args = parser.parse_args()

    def parser_name_formatter(parser_name_arg):
        parser_name, *others = parser_name_arg.split("-")
        return f"{parser_name}-{'-'.join(others)}"

    args.parser_names = list(map(parser_name_formatter, args.parser_names)) if args.parser_names else None

    return args
