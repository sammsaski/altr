import os
import streamlit as st
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from altru.zillow.zillow_scraper import ZillowScraper

st.title('Run Audit')

# authenticate user first
if st.session_state['authentication_status']:

    username = st.session_state['username']

    # get the api key or prompt the user to input a key.
    db = firestore.Client.from_service_account_json(os.getcwd() + '/firestore-key.json')

    audits = db.collection('audits').where(filter=FieldFilter('user', '==', username)).stream()
    audits_by_name = {x.to_dict()['name']: (x.to_dict(), x.id) for x in audits}

    option = st.selectbox(
        'Select an audit.',
        audits_by_name.keys(),
        key='audit_selection'
    )

    listing_sites_to_audit = st.multiselect(
        'Select the listing sites you would like to audit.',
        ['Zillow', 'Redfin', 'Trulia'],
        key='listing_sites_to_audit'
    )

    run_audit = st.button('Run!')

    if run_audit:
        # TODO: Implement the run audit functionality.
        pass

else:
    st.error('You must be logged in to access this page.')