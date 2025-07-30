import configparser
import os
import shutil
import sys
from pathlib import Path

from crawler_utils.test.crawler_tests.func.load_json import load_json_data

from .config_schemas import CrawlerArgumentsSchema, SpidersSpecificationSchema

config = configparser.ConfigParser()
config.read("scrapy.cfg")

project_name = config["deploy"]["project"]
project_path = os.path.abspath(project_name)
parent_path = os.path.dirname(project_path)
DIR_TO_PROJECT = Path(parent_path) / "test"

arguments_data = load_json_data(Path(DIR_TO_PROJECT) / "crawler_arguments.json", CrawlerArgumentsSchema)
spiders_specification = load_json_data(Path(DIR_TO_PROJECT) / "spiders_specification.json", SpidersSpecificationSchema)
SPIDER_NAMES = spiders_specification["spiders"]["spider_names"]

sys.path.append(os.path.abspath(DIR_TO_PROJECT))


def configure_crawler_settings(parser_name, tmp_dir: Path, mock_mode_enabled=False, create_test_data_enabled=False):
    """
    Configures Scrapy settings based on mode.

    Args:
        parser_name (str): The name of the parser for which the settings are being configured.
        tmp_dir (Path): Path to the temporary directory where logs and output files will be saved.
        mock_mode_enabled (bool, optional): Whether mock mode is enabled. If enabled, caching settings will be applied.
                                             Defaults to False.

    Returns:
        dict: A dictionary of settings that will be passed to Scrapy for this run.

    """
    BASE_DIR = Path(sys.path[-1])
    settings = {}

    # output path
    output_path = tmp_dir / f"{parser_name}_items.json"
    output_path.unlink(missing_ok=True)
    settings["FEEDS"] = {output_path: {"format": "json"}}

    # credentials
    settings["CREDENTIALS_STORE"] = "file"
    CREDENTIALS_PATH = BASE_DIR / "credentials.json"
    settings["CREDENTIALS_PATH"] = CREDENTIALS_PATH

    # logging
    settings["LOG_FILE"] = tmp_dir / "test.log"
    settings["LOG_LEVEL"] = "DEBUG"
    settings["DISABLE_TOPLEVELFORMATTER"] = True

    if mock_mode_enabled or create_test_data_enabled:
        """
               If mock_mode_enabled is True, caching settings are activated to use pre-cached responses.
               This configuration:
                   - HTTPCACHE_IGNORE_MISSING=False: If the cache is missing, the parser makes a real request.
                   - HTTPCACHE_ENABLED=True: Enables the HTTP cache for reusing responses.
        """

        settings["HTTPCACHE_ENABLED"] = True

        if mock_mode_enabled:
            settings["HTTPCACHE_IGNORE_MISSING"] = True

        else:
            settings["HTTPCACHE_IGNORE_MISSING"] = False
            settings["DOWNLOAD_DELAY"] = 5

        settings["HTTPCACHE_POLICY"] = "scrapy.extensions.httpcache.DummyPolicy"
        settings["HTTPCACHE_EXPIRATION_SECS"] = 0
        cache_dir = BASE_DIR / "cache_response" / parser_name
        cache_dir.mkdir(parents=True, exist_ok=True)
        settings["HTTPCACHE_DIR"] = cache_dir

        if create_test_data_enabled:
            for item in cache_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)

    else:
        settings["DOWNLOAD_DELAY"] = 3

    return settings
