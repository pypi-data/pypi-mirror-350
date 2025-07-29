import streamlit as st
from state_of_the_art.tables.user_table import UserEntity, UserTable


def get_authenticator():
    users = UserTable().get_all_users()
    credentials_usernames = {
        user.email: {
            "name": user.name,
            "password": user.password_hash,
            "email": user.email
        }
        for user in users
    }
    import streamlit_authenticator as stauth
    authenticator = stauth.Authenticate({'usernames': credentials_usernames}, 'cookie_name', 'signature_key', 15)
    return authenticator

def setup_login():
    import streamlit as st
    if st.query_params.get('page', False) == 'create_account':
        render_create_account_ui()
        st.stop()

    if LoginInterface.get_session().is_logged_in():
        return
    authenticator = get_authenticator()
    LoginInterface.set_authenticator(authenticator)
    try:
        #with st.sidebar:
        #    st.link_button("Create New Account", "/?page=create_account")
        authenticator.login()
    except Exception as e:
        st.error(e)

    if st.session_state['authentication_status']:
        return
        
    if st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')
    st.stop()

class LoginInterface:
    """
    This class is a singleton that manages the login state of the user.
    """
    cached_sessions = None
    user_entity = None
    @staticmethod
    def get_session() -> 'LoginInterface':
        if LoginInterface.cached_sessions is None:
            LoginInterface.cached_sessions = {}

        if not LoginInterface.get_email() in LoginInterface.cached_sessions:
            LoginInterface.cached_sessions[LoginInterface.get_email()] = LoginInterface()

        return LoginInterface.cached_sessions[LoginInterface.get_email()]


    def get_user(self) -> UserEntity:
        if self.user_entity is None:    
            user_df = UserTable().read()
            filtered_df = user_df[user_df["email"] == LoginInterface.get_email()]
            if len(filtered_df) == 0:
                raise ValueError("User not found")
            self.user_entity = UserEntity.from_dict(filtered_df.iloc[0].to_dict())

        return self.user_entity

    @staticmethod
    def set_authenticator(authenticator):
        LoginInterface.authenticator = authenticator
    
    def get_authenticator(self):
        if not hasattr(self, 'authenticator'):
            self.authenticator = get_authenticator()
        return self.authenticator

    def is_logged_in(self) -> bool:
        return LoginInterface.get_email() is not None

    @staticmethod   
    def get_email():
        return st.session_state.get('email')




def render_create_account_ui():
    import streamlit as st
    
    # Use custom CSS to improve the appearance
    st.markdown("""
    <style>
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    .stButton > button {
        border-radius: 20px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the create account form
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>Create an Account</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Join us today!</p>", unsafe_allow_html=True)
        
        with st.form("create_account_form"):
            email = st.text_input('Email', placeholder='Enter your email')
            name = st.text_input('Name', placeholder='Enter your full name')
            password = st.text_input('Password', type='password', placeholder='Choose a strong password')
            
            submit = st.form_submit_button('Create Account')
        
        if submit:
            st.session_state['create_account'] = True
            with st.spinner("Creating account..."):
                try:
                    uuid = UserTable().add_user(email, password, name)
                    st.success("Account created successfully! Now you can log in.")
                except ValueError as e:
                    st.error(str(e))
        
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("Already have an account?")
        st.link_button('Log in', '/?page=login')
        st.markdown("</div>", unsafe_allow_html=True)
        st.empty()
