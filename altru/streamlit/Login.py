import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import os
import bcrypt

# hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

with open (os.getcwd() + '/altru/streamlit/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

login_tab, register_tab, forgot_tab = st.tabs(['Login', 'Register', 'Forgot Username/Password'])

with login_tab:
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        authenticator.logout('Logout', 'sidebar', key='unique_key')
        # st.write(f'Welcome *{name}*')
        # st.title('Some content')
        st.header(f'Welcome *{name}!*')
        st.success('You are already logged in.')
    elif authentication_status is False:
        st.error('Username/password is incorrect')
    # elif authentication_status is None:
    #     st.warning('Please enter your username and password')

with register_tab:
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)

with forgot_tab:
    try:
        username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
        if username_forgot_username:
            st.success('Username sent securely')
            # Username to be transferred to user securely
        elif username_forgot_username == False:
            st.error('Email not found')
    except Exception as e:
        st.error(e)

    try:
        username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
        if username_forgot_pw:
            st.success('New password sent securely')
            # Random password to be transferred to user securely
        elif username_forgot_pw == False:
            st.error('Username not found')
    except Exception as e:
        st.error(e)




