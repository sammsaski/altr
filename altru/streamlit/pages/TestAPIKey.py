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
# api_key = config['credentials']['usernames'][username]['api_key']

doc = db.collection('users').document(username)
api_key = doc.get().to_dict()['api_key']

st.subheader('Submit/Edit Scraper API Key')

# if not config['credentials']['usernames'][username]['api_key']:
#     print('YAY!!!')    

# print(config['credentials']['usernames'][username])

view_key, add_key, edit_key, delete_key = st.tabs(['View', 'Add', 'Edit', 'Remove'])


with view_key:
    api_keys =  db.collection('api_keys').where(filter=FieldFilter('user', '==', username)).stream()
    api_keys = {x.to_dict()['name']: x.to_dict()['api_key'] for x in api_keys} # HACK: maybe not the most efficient
    option = st.selectbox(
        'Select an API Key to view.',
        [name for name in api_keys.keys()],
        key='view_key'
    )

    st.code(api_keys[option], language='markdown')

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
with edit_key:
    api_keys =  db.collection('api_keys').where(filter=FieldFilter('user', '==', username)).stream()
    name_to_id = {x.to_dict()['name']: x.id for x in api_keys}
    api_keys = {x.to_dict()['name']: (x.to_dict()['api_key'], x.id) for x in api_keys} # HACK: maybe not the most efficient
    option = st.selectbox(
        'Select an API Key to edit.',
        [name for name in api_keys.keys()],
        key='edit_key'
    )

    with st.form(key='edit_key_form', clear_on_submit=True):
        updated_api_key_name = st.text_input('API Key Name', value=option)
        updated_api_key = st.text_input('API Key', value=api_keys[option])
        submit_button = st.form_submit_button('Edit')
    
        if submit_button:
            db.collection('api_keys').document(name_to_id[option]).update({'name': updated_api_key_name})
            db.collection('api_keys').document(name_to_id[option]).update({'api_key': updated_api_key})
            st.experimental_rerun()

with delete_key:
    pass

# if not api_key:

#     # saves to api_key on 'enter'
#     # placeholder = st.empty()
#     # with placeholder.container():
#     api_key = st.text_input("Please input your Scraper API key.", key="api_key_form")
#     api_key_edit_button = st.button('Add', key='add_api_key_button')
#     if api_key_edit_button:
#         doc.update({'api_key': api_key})
#         st.experimental_rerun()
    
# else:
#     st.code(api_key, language='markdown')

