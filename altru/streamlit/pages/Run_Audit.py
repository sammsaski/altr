import os
import streamlit as st
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from altru.zillow.zillow_scraper import ZillowScraper
from altru.audit.audit import Audit

st.title('Run Audit')

# TODO: Implement this structure.
def audit_report_single_property_structure(address, price, bedrooms, bathrooms, sqft, acre, year_built):
    pass

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

    api_keys =  db.collection('api_keys').where(filter=FieldFilter('user', '==', username)).stream()
    api_keys = {x.to_dict()['name']: x.to_dict()['api_key'] for x in api_keys} # HACK: maybe not the most efficient
    api_key = st.selectbox(
        'Select an API Key to use.',
        [name for name in api_keys.keys()],
        key='audit_api_key'
    )

    api_key = db.collection('api_keys').where(filter=FieldFilter('user', '==', username)).where(
        filter=FieldFilter('name', '==', api_key)
    ).get()[0].get(field_path='api_key') # TODO: we need database guarantees that this will return only one object.

    properties = db.collection('audits').where(filter=FieldFilter('user', '==', username)).where(
        filter=FieldFilter('name', '==', option)
    ).get()[0].get(field_path='properties') # TODO: we need database guarantees that this will return only one object.

    # for property in properties:
    #     print(property.get())

    # NOTE :- use .get(field_path) on a DocumentSnapshot to get specific information.

    run_audit = st.button('Run!') # TODO: Disable button after run, UNLESS there is some input change.

    if run_audit:
        # TODO: Implement the run audit functionality.
        audit = Audit(
            properties=properties,
            listing_sites=listing_sites_to_audit,
            api_key=api_key
        )

        result, correct, total = audit.execute()
        
        # TODO: Copy over from streamlit/pages/comparison.py how to format the results of the audit.
        # for property in result:
        #     st.write(f'{property} : {result[property]}')

        for result_dict in result.values():
            for key, value in result_dict.items():
                # if key == 'address':
                #     st.subheader(value)
                # elif key == ''
                st.write(f'{key} : {value}')
            st.divider()
        
        st.subheader('Analytics')
        col = st.columns(3)
        col[0].metric('accuracy', '{:.2f}'.format(correct / total * 100) + '%')
        col[1].metric('correct', correct)
        col[2].metric('total', total)

else:
    st.error('You must be logged in to access this page.')