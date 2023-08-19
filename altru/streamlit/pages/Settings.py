import streamlit as st
import streamlit_authenticator as stauth
import os
import yaml
from yaml.loader import SafeLoader

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


    # TODO: Finish API Key work.
    # Add api key.
    api_key = config['credentials']['usernames'][username]['api_key'] # get the api key from yaml if it exists.

    if api_key:
        st.code(api_key, language='markdown')
    else:
        placeholder = st.empty()
        with placeholder.container():
            api_key_form = st.form(key='api_key_form')
            api_key_form.subheader('Add Scraper API Key')
            api_key = api_key_form.text_input("Please input your Scraper API key.")
            api_key_submit_button = api_key_form.form_submit_button(label='Submit')

            if api_key:
                placeholder.empty()
        st.code(api_key, language='markdown')


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