from crawler_utils.test.crawler_tests.func.settings import spiders_specification
from crawler_utils.test.crawler_tests.func.test_parser.parser_info import ParserInfo

parsers_to_check = [ParserInfo(**parser) for parser in spiders_specification["spiders"]["parsers"]]
