import os
from state_of_the_art.tables.base_table import BaseTable
from typing import Optional
import subprocess

class ReadBacklogTable(BaseTable):
    table_name = "read_backlog"
    schema = {
        "name": {"type": str}, 
        'resource_url': {"type": str}, 
        "comments": {"type": str}, 
        'priority': {"type": int}, 
        'progress': {"type": int},
        'time_spend_minutes': {"type": int},
    }

    def read_top(self):
        df = self.read()
        df = df.sort_values(by="priority", ascending=True)
        # filter out rows where progress is 100
        df = df[df['progress'] != 100]
        return df

    def add_or_update_record(self, name: str, new_values: dict):
        if 'comments' not in new_values:
            new_values['comments'] = ""
        if 'priority' not in new_values:
            new_values['priority'] = 0
        if 'progress' not in new_values:
            new_values['progress'] = 0
        if 'time_spend_minutes' not in new_values:
            new_values['time_spend_minutes'] = 0
        self.update_or_create(by_key="name", by_value=name, new_values=new_values)
        self.move_to_top(name)


    def add_time_spend(self, name: str, time_spend_minutes: int):
        df = self.read()
        df.loc[df['name'] == name, 'time_spend_minutes'] += time_spend_minutes
        self.twd.replace_df(self.table_name, df, dry_run=False)
        return df

    
    def move_to_top(self, name: str):
        # set priority to zero for the entry
        # increase the priority for all other entries
        df = self.read()
        # for all rows different from the one we want to move to top, increase the priority
        for index, row in df.iterrows():
            if row['name'] != name:
                df.at[index, 'priority'] += 1
        # set the priority to zero for the one we want to move to top
        df.loc[df['name'] == name, 'priority'] = 0
        self.twd.replace_df(self.table_name, df, dry_run=False)
        
        return df
    
    def mark_as_read(self, name: str):
        df = self.read()
        df.loc[df['name'] == name, 'progress'] = 100
        self.twd.replace_df(self.table_name, df, dry_run=False)
        return df
