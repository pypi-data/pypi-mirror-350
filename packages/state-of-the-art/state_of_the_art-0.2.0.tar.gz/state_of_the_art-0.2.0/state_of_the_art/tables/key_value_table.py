from typing import Any
from state_of_the_art.tables.base_table import BaseTable
from state_of_the_art.tables.changelog_table import Changelog


class KeyValueTable(BaseTable):
    table_name = "topics"
    schema = {
        "key": {"type": str},
        "value": {"type": str},
    }

    def update_or_create(self, key_name: str, new_value: str):
        return super().update_or_create(by_key='key', by_value=key_name, new_values={"value": new_value})

    def get_value(self, key: str):
        df = self.read()

        result = df[df["key"] == key]["value"]
        if result.empty:
            return None
        return result.values[0]
