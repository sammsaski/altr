from bs4 import BeautifulSoup
import requests
import subprocess
import re
import streamlit as st
from streamlit_extras.row import row

def curl_request(url):
    """
    Get the source code using Scraper API.
    """
    command = ['curl', url]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

class ZillowScraper:

    def __init__(self, api_key, url) -> None:
        """
        Retrieve the source code from the property on Zillow.
        """

        request_url = f'http://api.scraperapi.com?api_key={api_key}&url={url}'
        self.response = curl_request(url=request_url)        
        self.soup = BeautifulSoup(self.response, 'html.parser')
    
    def get_address(self) -> str:
        """
        Return the address.

        Unique to the address is that it is an 'h1' element, which makes things easy.
        """
        parent = self.soup.find('h1')
        return parent.text

    def get_price(self) -> str:
        """
        Return the price.


        """
        parent = self.soup.find('span', attrs={'data-testid': 'price'})
        children = parent.findChildren()
        
        return str(children[0].string)


    def get_bedrooms(self) -> str:
        """
        Return the number of bedrooms.

        Because bedrooms is structured like multiple other attributes of the house, we have to check
        specifics about how the bedrooms are listed.

        Hence, we know that the children as referred to by the code consists of 2--the value and the unit.
        """
        bedBathItems = self.soup.find_all('span', attrs={'data-testid': 'bed-bath-item'})

        for item in bedBathItems:
            children = item.findChildren()
            value = children[0].string
            unit = children[1].text.strip()

            if 'bd' == unit:
                return str(value)

    def get_bathrooms(self) -> str:
        """
        Return the number of bathrooms.

        Like bedrooms.
        """
        bedBathItems = self.soup.find_all('span', attrs={'data-testid': 'bed-bath-item'})

        for item in bedBathItems:
            children = item.findChildren()
            value = children[0].string
            unit = children[1].text.strip()

            if 'ba' == unit:
                return str(value)

    def get_sqft(self) -> str:
        """
        Return the interior square footage.

        Like bedrooms.
        """
        bedBathItems = self.soup.find_all('span', attrs={'data-testid': 'bed-bath-item'})

        for item in bedBathItems:
            children = item.findChildren()
            value = children[0].string
            unit = children[1].text.strip()

            if 'sqft' == unit:
                return str(value)
            
    def get_acre(self) -> str:
        """
        NOTE: Finding an element in bs4 based on the text in the tag i.e. <p>Hello</p> trying to find the element with "Hello".

        """
        element = self.soup.find('span', text=re.compile(r'\d*\.\d* Acres?'))
        return str(element.string)

    def get_year_built(self) -> str:
        """
        NOTE: Finding an element in bs4 based on the text in the tag i.e. <p>Hello</p> trying to find the element with "Hello".
        """
        element = self.soup.find('span', text=re.compile(r'Built in \d\d\d\d'))
        return element.string[9:]

    def execute(self) -> dict:
        return {
            'address': self.get_address(),
            'price': self.get_price(),
            'bedrooms': self.get_bedrooms(),
            'bathrooms': self.get_bathrooms(),
            'sqft': self.get_sqft(),
            'acre': self.get_acre(),
            'year_built': self.get_year_built(),
        }

    @staticmethod
    def display(data: dict) -> None:
        
        st.caption(f'Displaying data for...')
        st.subheader(f':blue[{data["address"]}]')

        property_details = row([3, 2, 2])
        property_details2 = row([3, 2, 2])
        property_details.metric('Price', data['price'])
        property_details.metric('Bedrooms', data['bedrooms'])
        property_details.metric('Bathrooms', data['bathrooms'])
        property_details2.metric('Square Footage', data['sqft'])
        property_details2.metric('Acreage', data['acre'])
        property_details2.metric('Year Built', data['year_built'])