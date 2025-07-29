import json
from csv import DictWriter
from io import StringIO
from pathlib import Path
from typing import Any, TypedDict

type JsonDict = dict[str, Any]

type DictOfJsonDicts = dict[str, JsonDict]
type ListOfJsonDicts = list[JsonDict]


class DictOfJsonDictsDiffUpdate(TypedDict):
    old: JsonDict
    new: JsonDict


class DictOfJsonDictsDiff(TypedDict):
    deletes: dict[str, JsonDict]
    inserts: dict[str, JsonDict]
    updates: dict[str, DictOfJsonDictsDiffUpdate]


class ListOfJsonDictsDiff(TypedDict):
    deletes: list[JsonDict]
    inserts: list[JsonDict]


def flatten(data: Any) -> Any:
    def flatten_rec(data: Any, path: str) -> None:
        if isinstance(data, dict):
            for k, v in data.items():
                flatten_rec(v, path + (f".{k}" if path else k))
        elif isinstance(data, list):
            for i, v in enumerate(data):
                flatten_rec(v, path + f"[{i}]")
        else:
            flatten_dict[path or "."] = data

    flatten_dict: JsonDict = {}
    flatten_rec(data, "")
    return flatten_dict


def json_to_csv(
    data: DictOfJsonDicts | ListOfJsonDicts,
    /,
    csv_path: Path | str | None = None,
    *,
    key_field_name: str = "_key",
) -> str:
    if isinstance(data, dict):
        data = [
            {
                # In case there is already a key field in each record,
                # the new key field will be overwritten.
                # It is okay though as the existing key field is likely
                # serving the purpose of containing keys.
                key_field_name: key,
                **value,
            }
            for key, value in data.items()
        ]

    fields: set[str] = set()
    for record in data:
        fields.update(record.keys())

    sio = StringIO()

    writer = DictWriter(sio, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)

    csv_str: str = sio.getvalue()

    if csv_path:
        Path(csv_path).write_text(csv_str)

    return csv_str


def dict_of_json_dicts_diff(
    old: DictOfJsonDicts,
    new: DictOfJsonDicts,
) -> DictOfJsonDictsDiff:
    inserts: dict[str, JsonDict] = {}
    updates: dict[str, DictOfJsonDictsDiffUpdate] = {}

    for new_key, new_value in new.items():
        old_value: dict[str, Any] | None = old.get(new_key, None)
        if old_value is None:
            inserts[new_key] = new_value
        elif json.dumps(old_value) != json.dumps(new_value):
            updates[new_key] = {
                "old": old_value,
                "new": new_value,
            }

    deletes: dict[str, JsonDict] = {
        old_key: old_value
        for old_key, old_value in old.items()
        if old_key not in new
    }

    return {
        "deletes": deletes,
        "inserts": inserts,
        "updates": updates,
    }


def list_of_json_dicts_diff(
    old: ListOfJsonDicts,
    new: ListOfJsonDicts,
) -> ListOfJsonDictsDiff:
    old_dict: DictOfJsonDicts = {
        json.dumps(d): d
        for d in old
    }
    new_dict: DictOfJsonDicts = {
        json.dumps(d): d
        for d in new
    }

    inserts: list[JsonDict] = [
        new_value
        for new_key, new_value in new_dict.items()
        if new_key not in old_dict
    ]
    deletes: list[JsonDict] = [
        old_value
        for old_key, old_value in old_dict.items()
        if old_key not in new_dict
    ]

    return {
        "deletes": deletes,
        "inserts": inserts,
    }
