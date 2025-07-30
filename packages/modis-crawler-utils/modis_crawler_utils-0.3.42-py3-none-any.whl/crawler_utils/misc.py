from typing import Any, Union

from scrapy.exceptions import NotConfigured
from scrapy.utils.misc import create_instance, load_object


def create_instance_from_settings(crawler, settings, setting_key, aliases, defaults):
    def load(cls_or_path):
        cls = load_object(cls_or_path)
        return create_instance(cls, settings=settings, crawler=crawler)

    if obj_name := settings.get(setting_key):
        obj_type = aliases.get(obj_name, obj_name)
        return load(obj_type)
    for obj_type in defaults:
        try:
            return load(obj_type)
        except NotConfigured:
            pass


def compact(container: Union[dict, list],
            exclude_none: bool = True,
            exclude_empty_types: tuple[type, ...] = (list, dict, str)) -> dict:
    def _to_be_removed(value: Any) -> bool:
        if exclude_none and value is None:
            return True
        if exclude_empty_types and isinstance(value, exclude_empty_types) and not value:
            return True
        return False

    def _compact(data):
        if isinstance(data, dict):
            return {
                key: compact_value for key, value in data.items()
                if not _to_be_removed(compact_value := _compact(value))
            }
        if isinstance(data, list):
            return [
                compact_value for value in data
                if not _to_be_removed(compact_value := _compact(value))
            ]
        return data

    return _compact(container)
