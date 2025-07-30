import sys
from pathlib import Path


class TestingArgumentsError(Exception):
    pass


class ReferenceDataError(Exception):
    pass


class LimitNotRegistred(Exception):
    pass


class MultipleTestingArgumentsNotSupported(TestingArgumentsError):
    def __init__(self):
        arguments_path = Path(sys.path[-1]).joinpath("crawler_arguments.json")

        arguments_path = arguments_path.relative_to(Path.cwd())
        err_msg = f"""Currently testing system doesn't support several sets of arguments for the same parser.
        You cannot create several test cases for one parser. Check {arguments_path}."""
        super().__init__(err_msg)
