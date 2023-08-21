import streamlit as st
import streamlit_authenticator as stauth
import os
import yaml
from yaml.loader import SafeLoader
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

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

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json(os.getcwd() + '/firestore-key.json')

# TODO: use session state NOT config file for loading api_key

username = st.session_state['username']
doc = db.collection('users').document(username)
api_key = doc.get().to_dict()['api_key']

st.subheader('Submit/Edit Scraper API Key')

view_key, add_key, edit_key, delete_key = st.tabs(['View', 'Add', 'Edit', 'Remove'])


#--------------------
#--- VIEW API_KEY ---
#--------------------
with view_key:
    api_keys =  db.collection('api_keys').where(filter=FieldFilter('user', '==', username)).stream()
    api_keys = {x.to_dict()['name']: x.to_dict()['api_key'] for x in api_keys} # HACK: maybe not the most efficient
    option = st.selectbox(
        'Select an API Key to view.',
        [name for name in api_keys.keys()],
        key='view_key'
    )

    st.code(api_keys[option], language='markdown')


#-------------------
#--- ADD API_KEY ---
#-------------------
with add_key:
    st.write('After adding your API key, please navigate to the `View` tab to ensure that the API key was added successfully.')

    with st.form(key='add_api_key_form', clear_on_submit=True):
        api_key = st.text_input("Please input your Scraper API key.", key="api_key_form")
        api_key_name = st.text_input("Please give your API key a name.", key='api_key_name')
        submit_button = st.form_submit_button('Submit')

        if submit_button:
            if not api_key:
                st.error('API key addition failed: you must enter an API key before submitting. Please try again.')
            elif not api_key_name:
                st.error('API key addition failed: you must give your API key a name. Please try again.')
            else:   
                db.collection('api_keys').add({'user': username, 'api_key': api_key, 'name': api_key_name})
                st.success('Hooray! API key addition succeeded!')

# TODO: FIX THIS
#--------------------
#--- EDIT API_KEY ---
#--------------------
with edit_key:
    api_keys = db.collection('api_keys').where(filter=FieldFilter('user', '==', username)).stream()
    api_keys = {x.to_dict()['name']: (x.to_dict()['api_key'], x.id) for x in api_keys} # HACK: maybe not the most efficient

    option = st.selectbox(
        'Select an API Key to edit.',
        api_keys.keys(),
        key='edit_key'
    )

    with st.form(key='edit_key_form', clear_on_submit=True):
        updated_api_key_name = st.text_input('API Key Name', value=option)
        updated_api_key = st.text_input('API Key', value=api_keys[option][0])
        submit_button = st.form_submit_button('Edit')
    
        if submit_button:
            db.collection('api_keys').document(api_keys[option][1]).update({'name': updated_api_key_name})
            db.collection('api_keys').document(api_keys[option][1]).update({'api_key': updated_api_key})
            st.experimental_rerun()

#----------------------
#--- DELETE API_KEY ---
#----------------------
with delete_key:
    api_keys = db.collection('api_keys').where(filter=FieldFilter('user', '==', username)).stream()
    api_keys = {x.to_dict()['name']: (x.to_dict()['api_key'], x.id) for x in api_keys} # HACK: maybe not the most efficient

    option = st.selectbox(
        'Select an API Key to edit.',
        api_keys.keys(),
        key='delete_key'
    )

    st.code(api_keys[option][0], language='markdown')

    delete_button = st.button('Delete')

    if delete_button:
        # delete the selected api_key
        db.collection('api_keys').document(api_keys[option][1]).delete()

        # reload the page
        st.experimental_rerun()
