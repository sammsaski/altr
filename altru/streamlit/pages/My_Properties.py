import streamlit as st
import streamlit_authenticator as stauth
import os
import yaml
from yaml.loader import SafeLoader
# from streamlit_extras.dataframe_explorer import dataframe_explorer
from typing import Dict, Any
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from streamlit_extras.grid import grid
import datetime
from streamlit_extras.row import row
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from streamlit_extras.stylable_container import stylable_container
from st_aggrid import AgGrid, GridOptionsBuilder

# TODO: Add support for links (zillow, redfin, etc.)


MAP_ATTRIBUTE_TO_DB_KEY = {
    'Address': 'address',
    'Price': 'price',
    'Bedrooms': 'bedrooms',
    'Bathrooms': 'bathrooms',
    'Square Footage': 'sqft',
    'Acreage': 'acre',
    'Year Built': 'year_built'
}


# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json(os.getcwd() + '/firestore-key.json')

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

st.title("Manage Properties")

### LOGOUT SEQUENCE PT. 2 ###
if st.session_state["authentication_status"]:

    # get the username from the session
    username = st.session_state['username']

    if not username:
        st.error("Please login to access this page.")

    view_property, create_property, edit_property, delete_property = st.tabs(['View', 'Create', 'Edit', 'Remove'])

    data = config['credentials']['usernames'][username]['properties']

    # TODO: Change the column names
    dataframe = pd.DataFrame.from_dict(data=data, orient='index')

    # TODO: View properties
    # TODO: Edit the table view.
    with view_property:
        docs = db.collection('properties').stream() # this gets all documents in 'properties'
        columns = MAP_ATTRIBUTE_TO_DB_KEY.values()
        items = list(map(lambda x: {**x.to_dict(), 'id': x.id}, docs))
        dataframe = pd.DataFrame(items, columns=columns)
        dataframe.columns = MAP_ATTRIBUTE_TO_DB_KEY.keys()

        AgGrid(
            dataframe.head(50),
            gridOptions=GridOptionsBuilder.from_dataframe(dataframe).build(),
        )


    # TODO: Add a property
    with create_property:
        with st.form(key='create_property_form', clear_on_submit=True):
            # address = st.text_input('Address')
            address_cols = st.columns([6, 4, 2, 2])
            address_cols[0].text_input('Street Address', key='street_address')
            address_cols[1].text_input('County', key='county')
            address_cols[2].selectbox('State', (['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']), key='state')
            address_cols[3].text_input('Zip Code', key='zip_code')

            price = st.number_input('Price')
            bedrooms = st.number_input('Bedrooms', value=0, step=1)
            bathrooms = st.number_input('Bathrooms', value=0, step=1)
            sqft = st.number_input('Sqft', value=0, step=1)
            acre = st.number_input('Acreage', value=0.00)
            year_built = st.number_input('Year Built', value=int(datetime.date.today().year))

            submit_button = st.form_submit_button('Submit')

            if submit_button:
                ss = st.session_state # save the session state for this
                address = f'{ss["street_address"]}, {ss["county"]}, {ss["state"]} {ss["zip_code"]}'

                data = {
                    'address': address,
                    'price': price,
                    'bedrooms': bedrooms,
                    'bathrooms': bathrooms,
                    'sqft': sqft,
                    'acre': acre,
                    'year_built': year_built,
                    'user': username
                }
                db.collection('properties').add(data)

    # TODO: Edit a property
    with edit_property:
        # TODO: Make sure this is limited to only the users properties
        # first need to get a property, then update it
        docs = db.collection('properties').stream() # this gets all documents in 'properties'
        docs_dict = {doc.to_dict()['address']: doc.id for doc in docs}
        
        option = st.selectbox(
                'Select a property.',
                docs_dict.keys(),
                key='edit_option'
        )

        property_id = docs_dict[option]
        property = db.collection('properties').document(property_id).get().to_dict()
        
        # Show the property details
        property_details = row([3, 2, 2])
        property_details2 = row([3, 2, 2])
        property_details.metric('Price', property['price'])
        property_details.metric('Bedrooms', property['bedrooms'])
        property_details.metric('Bathrooms', property['bathrooms'])
        property_details2.metric('Square Footage', property['sqft'])
        property_details2.metric('Acreage', property['acre'])
        property_details2.metric('Year Built', property['year_built'])

        # Choose the attribute to edit
        attribute = st.selectbox(
            'Select an attribute.',
            ['Address', 'Price', 'Bedrooms', 'Bathrooms', 'Square Footage', 'Acreage', 'Year Built'],
            key='attr_option'
        )

        attribute = MAP_ATTRIBUTE_TO_DB_KEY[attribute]

        updated_attribute_value = None # placeholder

        if attribute == 'address':
            address_cols = st.columns([6, 4, 2, 2])
            address_cols[0].text_input('Street Address', key='edit_street_address')
            address_cols[1].text_input('County', key='edit_county')
            address_cols[2].selectbox('State', (['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']), key='edit_state')
            address_cols[3].text_input('Zip Code', key='edit_zip_code')

            ss = st.session_state # save the session state for this
            updated_attribute_value = f'{ss["street_address"]}, {ss["county"]}, {ss["state"]} {ss["zip_code"]}'
        elif attribute == 'acre':
            updated_attribute_value = st.number_input('Acreage', value=0.00, label_visibility='collapsed')
        else:
            # TODO: Normalize database values and then come back and use the commented code to
            #       use the old value as the placeholder for the input.
            # attribute = MAP_ATTRIBUTE_TO_DB_KEY[attribute]
            # old_value = str(property[attribute])
            updated_attribute_value = st.number_input(attribute, value=0, step=1, label_visibility='collapsed')

        edit_button = st.button('Edit', key='edit_button')

        if edit_button:
            db.collection('properties').document(property_id).update({attribute: updated_attribute_value})
            st.experimental_rerun()

    # TODO: Remove a property
    with delete_property:
        # first need to get a property, then delete it
        # temp = db.collection('properties').stream() # this gets all documents in 'properties'
        # first need to get a property, then update it
        docs = db.collection('properties').stream() # this gets all documents in 'properties'
        docs_dict = {doc.to_dict()['address']: doc.id for doc in docs}
        
        option = st.selectbox(
                'Select a property.',
                docs_dict.keys(),
                key='delete_option'
        )

        property_id = docs_dict[option]
        property = db.collection('properties').document(property_id).get().to_dict()
        
        property_details = row([3, 2, 2])
        property_details2 = row([3, 2, 2])
        property_details.metric('Price', property['price'])
        property_details.metric('Bedrooms', property['bedrooms'])
        property_details.metric('Bathrooms', property['bathrooms'])
        property_details2.metric('Square Footage', property['sqft'])
        property_details2.metric('Acreage', property['acre'])
        property_details2.metric('Year Built', property['year_built'])

        delete_button = st.button('Delete')

        if delete_button:
            # delete the selected property
            db.collection('properties').document(property_id).delete()

            # reload the page update with the deletion
            st.experimental_rerun()


    
    authenticator.logout('Logout', 'sidebar', key='unique_key')
### END OF LOGOUT SEQUENCE ###
else:
    st.error('You are not logged in. Please login to edit your settings.')