import shutil
import sys
import tempfile
from pathlib import Path

import pytest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.reactor import install_reactor

from crawler_utils.test.crawler_tests.func.settings import SPIDER_NAMES, configure_crawler_settings
from crawler_utils.test.crawler_tests.func.utils import (
    get_args,
    get_args_by_parser_names,
    parse_arguments,
    setup_logger,
    timing_decorator,
)
from crawler_utils.test.crawler_tests.spider_logging import log_init

install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
logger = setup_logger()
PARSER_NAME_INDEX = 1
DIR_TO_TESTS = Path(__file__).resolve().parent


def move_tmp_files_to_output(tmp_dir: Path, output_dir: Path, args):
    """
    Moves temporary files from the given temporary directory to the output directory.

    Args:
        tmp_dir (Path): Path to the temporary directory containing generated files.
        output_dir (Path): Path to the output directory where files will be moved.

    """
    if not tmp_dir.exists():
        logger.error(f"Temporary directory {tmp_dir} does not exist!")

    output_dir.mkdir(exist_ok=True, parents=True)
    for file in tmp_dir.iterdir():
        output_path = output_dir / file.name
        shutil.move(file, output_path)

    logger.info(f"Moving files from {tmp_dir} to {output_dir}")


def run_spider(
    crawler_process: CrawlerProcess,
    spider_name: str,
    spider_arg: list[str],
    tmp_dir: Path,
    mock_mode_enabled: bool,
    create_test_data_enabled: bool,
):
    """
    Runs  spiders with the provided arguments and settings.

    Args:
        crawler_process (CrawlerProcess): Scrapy's CrawlerProcess to manage spider execution.
        spider_name (str): Name of the spider to run.
        spider_arg (List[str]): List of arguments for the spider in the form 'key=value'.
        tmp_dir (Path): Path to the temporary directory used for output.
        mock_mode_enabled (bool): Flag whether mock mode is enabled for the spiders.

    """
    parser_name = spider_arg[PARSER_NAME_INDEX].split("=")[0]
    settings = get_project_settings()
    new_settings = configure_crawler_settings(parser_name, tmp_dir, mock_mode_enabled, create_test_data_enabled)
    settings.update(new_settings)
    spider = crawler_process.spider_loader.load(spider_name)
    spider.custom_settings = spider.custom_settings or {}
    spider.custom_settings.update(new_settings)
    log_init(settings, parser_name)
    spider_arg = {arg.split("=")[0]: arg.split("=")[1] for arg in spider_arg}
    crawler_process.crawl(spider, **spider_arg)
    logger.info(f"Run spider {spider_name} with arguments {spider_arg}")


def run_crawler_process(
    spider_args_list: list[list[str]], tmp_dir: Path, mock_mode_enabled: bool, create_test_data_enabled: bool
):
    """
    Runs of spiders based on the provided list of spider arguments.

    Args:
        spider_args_list (List[List[str]]): List of spider arguments for each spider.
        tmp_dir (Path): Path to the temporary directory used for output.
        mock_mode_enabled (bool): Flag whether mock mode is enabled for the spiders.

    """
    project_settings = get_project_settings()
    pipelines_from_project_settings = project_settings.get("ITEM_PIPELINES", {})
    pipe_keywords = ("FilesPipelines")
    pipe_to_deletion = {
        pipe_name
        for pipe_name in pipelines_from_project_settings
        if any(keyword in pipe_name for keyword in pipe_keywords)
    }
    deleted_pipes = {pipe: pipelines_from_project_settings.pop(pipe, None) for pipe in pipe_to_deletion}
    disabled = [pipe for pipe, val in deleted_pipes.items() if val is not None]
    logger.info(f"Pipelines {disabled} were disabled for testing purposes.")

    project_settings.set("ITEM_PIPELINES", pipelines_from_project_settings)
    process = CrawlerProcess(project_settings)
    for spider_args in spider_args_list:
        field_name = "ARGUMENTS_FOR_MOCK_TESTS" if mock_mode_enabled else "ARGUMENTS_FOR_LIVE_TESTS"
        assert spider_args, (
            f"There are no argument for test running in {field_name} field in configuration. Tests will be aborted!"
        )
        spider_name = (
            SPIDER_NAMES.get("search") if "search" in spider_args[PARSER_NAME_INDEX] else SPIDER_NAMES.get("target")
        )

        run_spider(process, spider_name, spider_args, tmp_dir, mock_mode_enabled, create_test_data_enabled)

    process.start()


def run_tests(args, tmp_dir: Path):
    """
    Executes pytest tests  based on the script arguments.

    Args:
        args:  arguments, parsed by the argument parser.
        tmp_dir (Path): Path to the temporary directory used for testing.

    """
    custom_args = []

    if args.parser_names:
        or_string = " or ".join(args.parser_names)
        custom_args.append(f"-f {or_string}")

    if args.mock_mode:
        custom_args.append("--mock-mode")

    custom_args.append(f"--input-dir={tmp_dir!s}")
    pytest.main([str(DIR_TO_TESTS), "--tb=short", *custom_args])


@timing_decorator
def main():
    """
    Entry point for the run parsers and test execution.

    Args:
        args: Parsed command-line arguments  (--mock-mode, --create_test_data).
        DIR_TO_PROJECT: Path to the project directory .

    """
    args = parse_arguments()

    with tempfile.TemporaryDirectory() as output_dir:
        tmp_dir = Path(output_dir)
        crawling_args = (
            get_args_by_parser_names(args.parser_names, args.mock_mode)
            if args.parser_names
            else get_args(args.mock_mode, args.create_test_data)
        )
        run_crawler_process(crawling_args, tmp_dir, args.mock_mode, args.create_test_data)

        if args.create_test_data or args.save_items:
            output_path = Path(sys.path[-1]) / Path(args.output_items_dir)
            move_tmp_files_to_output(tmp_dir, output_path, args)

        if not args.create_test_data:
            run_tests(args, tmp_dir)


if __name__ == "__main__":
    main()
