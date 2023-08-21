import os
import streamlit as st
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from altru.zillow.zillow_scraper import ZillowScraper


def test_comparison(address_or_url):
    print(address_or_url)
    


st.title('Playground')

# TODO: Add logout capability.

# instantiate session state for receiving the URL/Address input.
if 'Address' not in st.session_state:
    st.session_state['Address'] = ''
if 'URL' not in st.session_state:
    st.session_state['URL'] = ''

# authenticate the user first
if st.session_state['authentication_status']:

    username = st.session_state['username']

    # get the api key or prompt the user to input a key.
    db = firestore.Client.from_service_account_json(os.getcwd() + '/firestore-key.json')

    api_keys = db.collection('api_keys').where(filter=FieldFilter('user', '==', username)).stream()
    api_keys = {x.to_dict()['name']: x.to_dict()['api_key'] for x in api_keys} # HACK: maybe not the most efficient

    api_key = None # placeholder

    # if the user has at least one api_key
    if api_keys:
        # prompt the user to select an api_key to choose from
        option = st.selectbox(
            'Select an API Key to use.',
            [name for name in api_keys.keys()],
            key='view_key_playground'
        )

        api_key = api_keys[option]
    
    # if the user does not have an api_key
    else:
        st.error('Please add an API key to your account before using the `Playground`.')

    # once validated, allow the user to enter a url or address
    choice = st.selectbox("Choose your preferred input.", ["URL", "Address"])

    address, url = None, None # instantiate address + URL

    # URL Search
    if choice == "URL":
        url = st.text_input("Please list the full URL (including `https://www.<rest of url>`)")

    # Address Search
    if choice == "Address": # TODO: use the address to find the URL
        address = st.text_input("Please list the full address in the following format: `<Street>, <County>, <State> <Zip>`")

    # select the listing sites you would like to search.
    listing_sites = st.multiselect(
        'Please select the listing site(s) you would like to audit.',
        ['Zillow', 'Redfin', 'Trulia']
    ) # TODO: Allow the user to choose their own listing site. Would need AutoML to learn to scrape the data from the site.

    playground_button = st.button('Run Audit')

    if playground_button:
        property = ZillowScraper(api_key=api_key, url=url)
        property_data = property.execute()
        ZillowScraper.display(property_data)

    # run the comparison
    # TODO: Implement the comparison function on the submit.
    # See `test_comparison` for a good model of how it might be structured.

    # display the comparison
