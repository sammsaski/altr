import sys
import os
import streamlit as st

from altru.zillow.zillow_scraper import ZillowScraper


true_data = {
    'address': '88 Rose Way, Bridgehampton, NY 11932',
    'price': '$21,000,000',
    'bedrooms': '10',
    'bathrooms': '15',
    'sqft': '12,300',
    'acre': '1.5 Acres',
    'year_built': '2022'
}


st.title("Altru Listings")

api_key = None
api_key_container = st.empty()

# NOTE: Maybe try to add a way to validate the API key?
with api_key_container.container():
    api_key_form = st.form(key='api_key_form')
    api_key = api_key_form.text_input("Please input your Scraper API key.")
    api_key_submit_button = api_key_form.form_submit_button(label='Submit')
    
    if not api_key:
        st.stop()
    else:
        api_key_container.empty()

st.success('Thank you for submitting your Scraper API key.')


if api_key:

    # Let user choose whether to search by URL or by address.
    choice = st.selectbox("Choose your preferred input.", ["URL", "Address"])

    # URL Search
    if choice == "URL":
        url_form = st.form(key='url_form')
        url = url_form.text_input("Please list the full URL (including `https://www.<rest of url>`)")
        url_submit_button = url_form.form_submit_button(label='Submit')

        # if a URL has been submitted
        if url_submit_button:
            zs = ZillowScraper(api_key, url)
            data = zs.execute()

            with st.container():

                for key, value in data.items():
                    x, y = st.columns(2)
                    with x:
                        st.metric(key, value)
                    with y:
                        st.metric(key, true_data[key])

                # st.metric('Address', data['address'])
                # st.metric('Price', data['price'])
                # st.metric('Bedrooms', data['bedrooms'])
                # st.metric('Bathrooms', data['bathrooms'])
                # st.metric('Interior Square Footage', data['sqft'])
                # st.metric('Acreage', data['acre'])
                # st.metric('Year Built', data['year_built'])


    # Address Search
    if choice == "Address":
        address_form = st.form(key='address_form')
        address = address_form.text_input("Please list the full address in the following format: `<Street>, <County>, <State> <Zip>`")
        address_submit_button = address_form.form_submit_button(label='Submit')
