import streamlit as st
import streamlit_authenticator as stauth
import os
import yaml
from yaml.loader import SafeLoader

# TODO: Implement Firestore into this page.

### METHODS ###

###############

### LOGOUT SEQUENCE PT. 1 ###
with open (os.getcwd() + '/altru/streamlit/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
###

st.title("Settings")

### LOGOUT SEQUENCE PT. 2 ###
if st.session_state["authentication_status"]:

    # get the username from the session
    username = st.session_state['username']

    try:
        if authenticator.reset_password(username, 'Reset password'):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)

    try:
        if authenticator.update_user_details(username, 'Update user details'):
            st.success('Entries updated successfully')
    except Exception as e:
        st.error(e)

    authenticator.logout('Logout', 'sidebar', key='unique_key')
### END OF LOGOUT SEQUENCE ###
else:
    st.error('You are not logged in. Please login to edit your settings.')