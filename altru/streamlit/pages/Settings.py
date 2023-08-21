import streamlit as st
import streamlit_authenticator as stauth
import os
import yaml
from yaml.loader import SafeLoader

### METHODS ###
def toggle_api_key_form():
    st.session_state.api_key_form_disabled = not st.session_state.api_key_form_disabled
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

    ### Rest of page goes here.
    if "api_key_form_disabled" not in st.session_state:
        st.session_state.api_key_form_disabled = False


    # TODO: Finish API Key work.
    # Add api key.
    api_key = config['credentials']['usernames'][username]['api_key'] # get the api key from yaml if it exists.

    if api_key:
        toggle_api_key_form()
        
    with st.form(key='api_key_form'):

        st.subheader('Add Scraper API Key')

        api_key = st.text_input("Please input your Scraper API key.", key="api_key_form")
        submit_button = st.form_submit_button(
            label='Submit', on_click=toggle_api_key_form, disabled=st.session_state.api_key_form_disabled
        )
            
    # update config file with api key.
    with open(os.getcwd() + '/altru/streamlit/config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


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