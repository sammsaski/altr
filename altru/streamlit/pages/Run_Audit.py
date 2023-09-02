import os
import streamlit as st
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from streamlit_extras.row import row

from altru.zillow.zillow_scraper import ZillowScraper
from altru.audit.audit import Audit
from altru.audit.display_data import format_string

ATTRS = ['address', 'price' , 'bedrooms', 'bathrooms', 'sqft', 'acre', 'year_built']

# Establish a connection to the database
db = firestore.Client.from_service_account_json(os.getcwd() + '/firestore-key.json')


st.title('Run Audit')

# Authenticate the user first
if st.session_state['authentication_status']:

    # Get the username of the user's active session
    username = st.session_state['username']

    # Get all of the user's audits
    audits = db.collection('audits').where(filter=FieldFilter('user', '==', username)).stream()
    audits_by_name = {x.to_dict()['name']: (x.to_dict(), x.id) for x in audits}

    # Prompt the user to select the audit they wish to perform
    # Save its `name`; to be used to GET the audit from the database
    option = st.selectbox(
        'Select an audit.',
        audits_by_name.keys(),
        key='audit_selection'
    )

    # Prompt the user to select the listing sites they wish to audit
    # And save them as a list
    listing_sites_to_audit = st.multiselect(
        'Select the listing sites you would like to audit.',
        ['Zillow', 'Redfin', 'Trulia', 'Homes.com'],
        key='listing_sites_to_audit'
    )

    # Prompt the user to select which API key they wish to use
    # And save it's `name` to `api_key` as a string
    api_keys =  db.collection('api_keys').where(filter=FieldFilter('user', '==', username)).stream()
    api_keys = {x.to_dict()['name']: x.to_dict()['api_key'] for x in api_keys} # HACK: maybe not the most efficient
    api_key = st.selectbox(
        'Select an API Key to use.',
        [name for name in api_keys.keys()],
        key='audit_api_key'
    )

    # GET the API key associated with the chosen API key name from the database
    api_key = db.collection('api_keys').where(filter=FieldFilter('user', '==', username)).where(
        filter=FieldFilter('name', '==', api_key)
    ).get()[0].get(field_path='api_key') # TODO: we need database guarantees that this will return only one object.

    # GET the properties associated with the chosen audit name from the database
    properties = db.collection('audits').where(filter=FieldFilter('user', '==', username)).where(
        filter=FieldFilter('name', '==', option)
    ).get()[0].get(field_path='properties') # TODO: we need database guarantees that this will return only one object.

    run_audit = st.button('Run!')

    if run_audit:

        # ---------------------
        # ----- RUN AUDIT -----
        # ---------------------
        audit = Audit(
            properties=properties,
            listing_sites=listing_sites_to_audit,
            api_key=api_key
        )

        result, correct, total = audit.execute()
        
        # ---------------------
        # ------ DISPLAY ------
        # ---------------------

        css = '''
            [data-testid="stCaptionContainer"] {
                padding-top: 15px;
            }
        '''

        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

        st.subheader('Analytics')
        col = st.columns(3)
        col[0].metric('accuracy', '{:.2f}'.format(correct / total * 100) + '%')
        col[1].metric('correct', correct)
        col[2].metric('total', total)

        st.divider()

        for i, result_dict in enumerate(result.values()):

            # retrieve the true data from the database + verify types
            true_data = properties[i].get().to_dict()

            for key, value in result_dict.items():
                if key in ATTRS:
                    if key == 'address':
                        col = st.columns([3, 14])
                        col[0].caption(key)
                        col[1].subheader(value)
                    else:
                        col = st.columns([3, 6, 2, 6])
                        col[0].caption(key)
                        col[1].subheader(format_string(key=key, value=true_data[key]))
                        col[2].subheader('▸')
                        col[3].subheader(value)

            st.divider()

else:
    st.error('You must be logged in to access this page.')