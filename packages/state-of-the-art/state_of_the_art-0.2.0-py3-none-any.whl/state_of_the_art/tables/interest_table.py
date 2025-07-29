import os
from state_of_the_art.tables.base_table import BaseTable
from state_of_the_art.tables.changelog_table import Changelog


class InterestTable(BaseTable):
    table_name = "topics"
    schema = {
        "name": {"type": str},
        "description": {"type": str},
        'position': {'type': int}
    }
    def __init__(self):
        super().__init__()

    def delete_by_name(self, name: str):
        self.delete_by(column="name", value=name)
        Changelog().add_log(message=f"Deleted interest {name}")

    def add_interest(self, name: str, description: str):
        self.add(name=name, description=description, position=0)
        self.move_to_top(name)
        Changelog().add_log(message=f"Added interest {name}")

    def move_to_top(self, name: str):
        # get current position
        df = self.read()
        # make current element 1 bigger than the biggest position
        position = df[df["name"] == name]["position"].values[0]
        position = df["position"].max() + 1
        df.loc[df["name"] == name, "position"] = position

        self.replace(df, dry_run=False)

    def move_to_bottom(self, name: str):
        df = self.read()
        # make current element 1 smaller than the smallest position
        position = df[df["name"] == name]["position"].values[0]
        position = df["position"].min() - 1
        df.loc[df["name"] == name, "position"] = position
        self.replace(df, dry_run=False)
    
    def read_sorted_by_position(self):
        df = self.read()
        # higher on top
        df = df.sort_values(by="position", ascending=False)
        return df
