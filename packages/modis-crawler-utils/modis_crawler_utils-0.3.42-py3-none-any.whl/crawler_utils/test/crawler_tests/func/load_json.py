import json
from pathlib import Path

import pydantic


def load_json_data(json_path: Path, json_schema: type[pydantic.BaseModel] | None = None) -> dict:
    if not json_path.is_file():
        msg = f"File '{json_path}' not found."
        raise FileNotFoundError(msg)

    try:
        json_data = json.loads(json_path.read_text(encoding="utf-8"))
        if not json_schema:
            return json_data
        return json_schema(**json_data).model_dump()
    except json.JSONDecodeError as err:
        msg = f"Failed to decode JSON from file '{json_path}': {err.msg}"
        raise ValueError(msg) from err
    except pydantic.ValidationError as err:
        msg = f"Validation failed for config file '{json_path}'"
        raise ValueError(msg) from err
