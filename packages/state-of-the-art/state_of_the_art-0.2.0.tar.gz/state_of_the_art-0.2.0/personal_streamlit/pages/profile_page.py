import time

start_time = time.time()
from state_of_the_art.infrastructure.datadog_utils import send_metric

from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page
initialize_page()
import streamlit as st

from state_of_the_art.streamlit_app.utils.login_utils import LoginInterface
from state_of_the_art.tables.user_table import UserTable


user_entity = LoginInterface.get_session().get_user()
st.title("Profile")
st.info("Edit your profile here including your email reports preferences.")
name = st.text_input("Your Name", value=user_entity.get_name())
email = st.text_input("Email", value=user_entity.get_email())
prompt = st.text_area("About me prompt", value=user_entity.get_prompt())
password = st.text_input("Password", type="password", value=user_entity.get_password_hash())

st.markdown("### Email subscription preferences:")
daily_email_enabled = st.checkbox("Daily email", value=user_entity.has_daily_email_enabled())
weekly_email_enabled = st.checkbox("Weekly email", value=user_entity.has_weekly_email_enabled())
monthly_email_enabled = st.checkbox("Monthly email", value=user_entity.has_monthly_email_enabled())

if st.button("Save Changes"):
    new_values = {
        'email': email,
        'prompt': prompt,
        'password_hash': password,
        'name': name,
        'daily_email_enabled': daily_email_enabled,
        'weekly_email_enabled': weekly_email_enabled,
        'monthly_email_enabled': monthly_email_enabled,
    }

    UserTable().update(by_key="tdw_uuid", by_value=user_entity.get_uuid(), new_values=new_values)
    st.success("Changes saved successfully")
    time.sleep(1)
    st.rerun()

send_metric("sota.profile_page.render_duration", time.time() - start_time)
