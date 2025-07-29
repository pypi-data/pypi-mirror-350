import streamlit as st
from personal_streamlit.utils.sidebar_utils import initialize_page

initialize_page()

from personal_streamlit.read_backlog.read_backlog_table import ReadBacklogTable

st.title("📚 Read Backlog")

@st.dialog("Add/Edit Resource")
def resource_dialog(resource_name=None, resource_url=None):
    
    new_resource_name = st.text_input("Resource Name", value=resource_name or "", placeholder="Enter the name of the resource")
    new_resource_url = st.text_input("Resource URL", value=resource_url or "", placeholder="Enter the URL of the resource")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Save", type="primary"):
            st.session_state.show_dialog = False

            new_values = {"name": new_resource_name, "resource_url": new_resource_url}
            ReadBacklogTable().add_or_update_record(resource_name, new_values)
            st.rerun()
    with col2:
        if st.button("Cancel"):
            st.session_state.show_dialog = False
            st.rerun()
    with col3:
        if resource_name and st.button("✅ Mark as Read", type="secondary"):
            ReadBacklogTable().mark_as_read(resource_name)
            st.session_state.show_dialog = False
            st.rerun()
    with col4:
        
        if st.button("🗑️", help="Remove resource") or st.session_state.get(f"confirm_remove_{resource_name}", False):
            st.session_state[f"confirm_remove_{resource_name}"] = True
            st.warning(f"Are you sure you want to remove '{resource_name}'?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes", key=f"confirm_remove_{resource_name}_button"):
                    ReadBacklogTable().delete_by(column="name", value=resource_name)
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"cancel_remove_{resource_name}"):
                    st.rerun()

# Button to open dialog for new resource
if st.button("➕ Add New Resource", type="primary"):
    resource_dialog()

# Display existing resources
df = ReadBacklogTable().read_top()
counter=0
for index, row in df.iterrows():
    counter+=1
    col1, col2, col3, col4 = st.columns([6, 1, 1, 1])
    with col1:
        time_spent = " ⏱️ "
        if row['time_spend_minutes'] > 0:
            hours = row['time_spend_minutes'] // 60
            minutes = row['time_spend_minutes'] % 60
            if hours > 0:
                time_spent = f" ⏱️ {hours}h"
            if minutes > 0:
                time_spent += f" {minutes}m"
        st.markdown(f"{counter}. [{row['name']}]({row['resource_url']}){time_spent}")
    with col2:
        if st.button("✏️", key=f"edit_{counter}", help="Edit resource"):
            resource_dialog(resource_name=row['name'], resource_url=row['resource_url'])
    with col3:
        if st.button("⬆️", key=f"move_top_{counter}", help="Move to top"):
            ReadBacklogTable().move_to_top(row['name'])
            st.rerun()
    with col4:
        if st.button("⏱️+5", key=f"add_time_{counter}", help="Add 5 minutes"):
            ReadBacklogTable().add_time_spend(row['name'], 5)
            st.rerun()

# Add Resource Modal
