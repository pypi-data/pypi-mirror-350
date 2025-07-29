import os
from state_of_the_art.tables.base_table import BaseTable
from typing import Optional
import subprocess

class EnergyTrackerTable(BaseTable):
    table_name = "energy_tracker"
    schema = {"energy_level": {"type": int}, "energy_description": {"type": str}}


    def add_record(self, energy_level: int, energy_description: str):
        print(f"Adding energy tracker record: {energy_level} {energy_description}")
        self.add(energy_level=energy_level, energy_description=energy_description)
