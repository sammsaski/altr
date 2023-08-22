from bs4 import BeautifulSoup
import requests
import subprocess
import re
from decimal import Decimal
import streamlit as st
from streamlit_extras.row import row

test_data = {
    'address': '99 Fairfield Pond Ln,\xa0Sagaponack, NY 11963', 
    'price': '$18,995,000', 
    'bedrooms': '9', 
    'bathrooms': '15', 
    'sqft': '12,205', 
    'acre': '2.07 Acres', 
    'year_built': '2016'
}

def curl_request(url):
    """
    Get the source code using Scraper API.
    """
    command = ['curl', url]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

class ZillowScraper:

    def __init__(self, api_key=None, url=None) -> None:
        """
        Instantiate a ZillowScraper object and (optionally) retrieve the source
        code from the property on Zillow.
        """
        if api_key and url:
            request_url = f'http://api.scraperapi.com?api_key={api_key}&url={url}'
            self.response = curl_request(url=request_url)        
            self.soup = BeautifulSoup(self.response, 'html.parser')

    def request_html(self, api_key, url) -> None:
        """
        Retrieve the source code of a specific property on Zillow.
        """
        request_url = f'http://api.scraperapi.com?api_key={api_key}&url={url}'
        self.response = curl_request(url=request_url)
        self.soup = BeautifulSoup(self.response, 'html.parser')

    def normalize_data(self, scraped_data) -> dict:
        data = {}

        for key, value in scraped_data.items():
            if key == 'address':
                # TODO: Convert address to its parts.
                # NOTE: For now, this is a workaround.
                data[key] = value.replace('\xa0', ' ') # must remove this '&nbsp;' character for comparison

            elif key == 'price':
                data[key] = float(Decimal(re.sub(r'[^\d.]', '', scraped_data[key]))) # must remove '$' and commas before casting to int

            elif key == 'bedrooms' or key == 'bathrooms':
                data[key] = int(scraped_data[key]) # convert to correct type

            elif key == 'sqft':
                data[key] = int(scraped_data[key].replace(',', '')) # must remove commas before casting to int

            elif key == 'acre':
                data[key] = float(re.sub(r'[^\d*.\d*]', '', scraped_data[key]).strip()) # Remove ' Acres' and cast to float

            elif key == 'year_built':
                data[key] = int(scraped_data[key])

            else:
                raise Exception(f'An unexpected value (key: {key}) has entered the scraped data.')
            
        return data
    
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


if __name__=="__main__":
    scraper = ZillowScraper()

    results = scraper.normalize_data(scraped_data=test_data)
    print(results)
