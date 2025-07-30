import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


TEST_DIR = "test"

DIRECTORIES = [
    "cache_response",
    "reference_items",
    "reference_items/live_reference_items",
    "reference_items/mock_reference_items",
]

JSON_FILES = {
    "spiders_specification.json.example": """
    spiders_specification.json содержит спецификации пауков и их параметры для настройки тестов.
    Спецификации пауков включают названия пауков, которые будут запускаться, названия парсеров с аргументами, а также информацию о выходных типах данных для каждого парсера.

    Example:
    {
        "spiders": {
            "parsers": [
                {
                    "parser_name": "user_posts",
                    "path_to_test_results": "get_user_posts_items.json",
                    "output_itemtypes": ["UserProfile", "GroupProfile", "Message"]
                }
            ],
            "spider_names": {
                "search": "vk_target_spider",
                "target": "vk_search_spider"
            }
        },
        "limits2type": {
            "community_followers": "user_profile",
            "user_posts": "post",
            "user_profiles_subscriptions": "group_profile"
        },
        "itemtype2id": {
            "comment": ["message_id"],
            "social_connection": ["from_id", "to_id"]
        }
    }
        """.strip(),
    "credentials.json.example": """
    credentials.json содержит учетные данные для авторизации.

    Example:
    {
        "credential_id": 1,
        "credential_type": "Account",
        "domain": "vk.com",
        "login": "your_login",
        "password": "your_password",
        "state": {
            "TIME_CREATED_TOKEN": 1234567890,
            "CLIENT_ID": 1,
            "TOKEN_EXPIRATION_TIME": 1234567890,
            "SESSION_TOKEN": "your_session_token"
        },
        "status": "Valid"
    }
        """.strip(),
    "crawler_arguments.json.example": """
    crawler_arguments.json содержит аргументы для mock-тестов и live тестов.
    Example:
    {
        "ARGUMENTS_FOR_MOCK_TESTS": {
            "vk_target_spider": [["url=https:vk.com/id138943024", "get_user_profile=True"]],
            "vk_search_spider": [["search_query=work", "get_community_search=True"]]
        },
        "ARGUMENTS_FOR_LIVE_TESTS": {
            "vk_target_spider": [["url=https:vk.com/makssidorov1", "get_user_profile=True"]],
            "vk_search_spider": [["search_query=work", "get_community_search=True"]]
        }
    }
        """.strip(),
}


def create_directories():
    for directory in DIRECTORIES:
        full_path = os.path.join(TEST_DIR, directory)
        os.makedirs(full_path, exist_ok=True)
        with open(os.path.join(full_path, "__init__.py"), "w") as f:
            f.write("\n")


def create_json_files():
    for file_name, content in JSON_FILES.items():
        file_path = os.path.join(TEST_DIR, file_name)

        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(content)

            logger.info(f"File {file_name} created successfully.")
        else:
            logger.info(f"File {file_name} already exists.")


def create_tests_directory():
    if os.path.exists(TEST_DIR):
        logger.info(f"Directory {TEST_DIR} already exists. Skipping creation.")
        return

    os.makedirs(TEST_DIR)
    logger.info(f"Created test directory: {TEST_DIR}")
    create_directories()
    create_json_files()


if __name__ == "__main__":
    create_tests_directory()
