import os
import pandas as pd
import streamlit as st
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from st_aggrid import AgGrid, GridOptionsBuilder

# TODO: NOTE THAT STREAMLIT REQUESTS THE DATA EVERY SINGLE TIME AN INPUT CHANGES OR IT REFRESHES.
#       TO RESOLVE THIS, DO SOME RESEARCH ON CACHING THE DATA RESULTS. THIS IS ADVANCED NO NEED
#       TO WORRY ABOUT IT YET.

MAP_ATTRIBUTE_TO_DB_KEY = {
    'Address': 'address',
    'Price': 'price',
    'Bedrooms': 'bedrooms',
    'Bathrooms': 'bathrooms',
    'Square Footage': 'sqft',
    'Acreage': 'acre',
    'Year Built': 'year_built'
}

st.title('Manage Audits')

view_audit, create_audit, delete_audit = st.tabs(['View', 'Create', 'Delete'])

# authenticate user first
if st.session_state['authentication_status']:

    username = st.session_state['username']

    # get the api key or prompt the user to input a key.
    db = firestore.Client.from_service_account_json(os.getcwd() + '/firestore-key.json')

    with view_audit:
        audits = db.collection('audits').where(filter=FieldFilter('user', '==', username)).stream()
        audits_by_name = {x.to_dict()['name']: x.to_dict() for x in audits}

        option = st.selectbox(
            'Select an audit.',
            audits_by_name.keys(),
            key='audit_view'
        )

        docs = audits_by_name[option].get('properties')
        columns = MAP_ATTRIBUTE_TO_DB_KEY.values()
        items = list(map(lambda x: {**x.get().to_dict(), 'id': x.id}, docs))
        dataframe = pd.DataFrame(items, columns=columns)
        dataframe.columns = MAP_ATTRIBUTE_TO_DB_KEY.keys()

        st.dataframe(dataframe)

    with create_audit:
        properties = db.collection('properties').where(filter=FieldFilter('user', '==', username)).stream()
        # TODO: Refactor this logic so that the audits_by_name isn't a tuple. There has to be a more
        #       verbose way to get the data that I want.
        properties_by_address = {x.to_dict()['address']: (x.to_dict(), x.id) for x in properties}

        audit_name = st.text_input('Please give your audit a name.', value='')

        st.subheader('↓')
        st.subheader('Now, build your audit.')

        properties_to_audit = st.multiselect(
            'Select the properties you would like to audit.',
            properties_by_address.keys()
        )

        # sites_to_audit = st.multiselect(
        #     'Select the listing sites you would like to audit.',
        #     ['Zillow', 'Redfin', 'Trulia']
        # )

        st.divider()

        st.caption('Listed below is the audit you wish to create.')
        # st.subheader(f'For {", ".join([f":blue[{site}]" for site in sites_to_audit])}...' + ' audit the following properties.')
        
        columns = MAP_ATTRIBUTE_TO_DB_KEY.values()
        # items = list(map(lambda x: {**x.get().to_dict(), 'id': x.id}, docs))
        items = [properties_by_address[address][0] for address in properties_to_audit]
        dataframe = pd.DataFrame(items, columns=columns)
        dataframe.columns = MAP_ATTRIBUTE_TO_DB_KEY.keys()

        st.dataframe(dataframe, use_container_width=True)

        st.write('If it looks good, click the button below to create your audit!')
        create_audit_button = st.button('Create')

        if create_audit_button:
            audit_data = {
                'properties': [db.collection('properties').document(properties_by_address[address][1]) for address in properties_to_audit],
                'name': audit_name,
                'user': username
            }
            db.collection('audits').add(audit_data)
            st.experimental_rerun()

    with delete_audit:
        audits = db.collection('audits').where(filter=FieldFilter('user', '==', username)).stream()
        audits_by_name = {x.to_dict()['name']: (x.to_dict(), x.id) for x in audits}

        option = st.selectbox(
            'Select an audit.',
            audits_by_name.keys(),
            key='audit_delete'
        )

        # TODO: Refactor this logic so that the audits_by_name isn't a tuple. There has to be a more
        #       verbose way to get the data that I want.
        docs = audits_by_name[option][0].get('properties')
        columns = MAP_ATTRIBUTE_TO_DB_KEY.values()
        items = list(map(lambda x: {**x.get().to_dict(), 'id': x.id}, docs))
        dataframe = pd.DataFrame(items, columns=columns)
        dataframe.columns = MAP_ATTRIBUTE_TO_DB_KEY.keys()

        st.dataframe(dataframe)

        delete_audit_button = st.button('Delete')

        if delete_audit_button:
            # delete the audit
            db.collection('audits').document(audits_by_name[option][1]).delete()
            
            # rerun the app
            st.experimental_rerun()


else:
    st.error('You must be logged in to access this page.')