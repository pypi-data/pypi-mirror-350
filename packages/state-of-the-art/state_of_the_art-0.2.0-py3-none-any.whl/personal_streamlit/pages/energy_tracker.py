
from enum import Enum
from typing import List
import streamlit as st
from state_of_the_art.energy_tracker.energy_tracker_table import EnergyTrackerTable
from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page
initialize_page()


st.title("Energy Tracker")

class EnergyLevels(Enum):
    VERY_LOW = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

    @staticmethod
    def get_descriptions() -> List[str]:
        return [
            "Very low",
            "Low",
            "Medium",
            "High",
            "Very high"
        ]
    @staticmethod
    def get_index_from_description(description: str) -> int:
        return EnergyLevels.get_descriptions().index(description)

energy_level = st.selectbox("Energy Level", EnergyLevels.get_descriptions(), index=2)
energy_level_index = EnergyLevels.get_index_from_description(energy_level)
energy_description = st.text_area("Record Description", height=100)
if st.button("Save"):
    energy_tracker_table = EnergyTrackerTable()
    energy_tracker_table.add_record(energy_level=energy_level_index, energy_description=energy_description)
    st.success("Record saved")



df = EnergyTrackerTable().read(recent_first=True)

st.write(df)
