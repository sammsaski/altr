from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import streamlit as st
from streamlit_extras.row import row
import subprocess

def curl_request(url) -> str:
    """Get the source code using Scraper API.

    Parameters
    ----------
    url : str
        The url of the property on the site whose data is being
            requested.

    Returns
    -------
    str :
        The retrieved source code from the curl request.
    """

    command = ['curl', url]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

class Scraper(ABC):
    """
    Template for an instance of a Scraper (i.e., ZillowScraper, TruliaScraper, etc.)
        and for any future scrapers.
    
    The goal of these scrapers is to take in an api_key and a url to a property and
        return the relevant data [address, price, bd, ba, sqft, acre, year_built]
        back to the client to show the user.
    """

    def __init__(self, api_key=None, url=None) -> None:
        """Create a Scraper and (optionally) get the source html.

        Parameters
        ----------
        api_key : str
            The Scraper API key to be used to request the site's html.
        
        url : str
            The url of the property on the site whose data is being
            requested.
        """
        if api_key and url:
            request_url = f'http://api.scraperapi.com?api_key={api_key}&url={url}'
            self.response = curl_request(url=request_url)        
            self.soup = BeautifulSoup(self.response, 'html.parser')

    def request_html(self, api_key, url) -> None:
        """Retrieve the source code of a specific property on Zillow.

        Additionally, associates the source code with the instance of
        the scraper object.

        Parameters
        ----------
        api_key : str
            The Scraper API key to be used to request the site's html.
        
        url : str
            The url of the property on the site whose data is being
            requested.
        """

        request_url = f'http://api.scraperapi.com?api_key={api_key}&url={url}'
        self.response = curl_request(url=request_url)
        self.soup = BeautifulSoup(self.response, 'html.parser')

    @abstractmethod
    def normalize_data(self, scraped_data) -> dict:
        """Normalize the data to data types of:
            'address': str
            'price': int
            'bedrooms': int
            'bathrooms': int
            'sqft': int
            'acre': float
            'year_built': int

        Parameters
        ----------
        scraped_data : dict
            The data scraped from the site structured as above.

        Returns
        -------
        dict
            The data type cast to the types defined above.
        """

        pass
    
    @abstractmethod
    def get_address(self) -> str:
        """Get the address from the source html.

        NOTE: Unique to the address is that it is an 'h1' element, which makes things easy.

        Returns
        -------
        str :
            A string representing the address from the property site.
        """

        pass

    @abstractmethod
    def get_price(self) -> str:
        """Get the price from the source html.

        Returns
        -------
        str :
            A string representing the price from the property site.
        """

        pass

    @abstractmethod
    def get_bedrooms(self) -> str:
        """Return the number of bedrooms from the source html.

        Returns
        -------
        str :
            A string representing the number of bedrooms from the
            property site.
        """
        
        pass

    @abstractmethod
    def get_bathrooms(self) -> str:
        """Return the number of bathrooms from the source html.

        Returns
        -------
        str :
            A string representing the nubmer of bathrooms from the
            property site.
        """
        
        pass

    @abstractmethod
    def get_sqft(self) -> str:
        """Return the interior square footage from the source html.

        Returns
        -------
        str :
            A string representing the interior square footage from the
            property site.
        """
        
        pass

    @abstractmethod
    def get_acre(self) -> str:
        """Return the acreage (lot size) from the source html.

        Returns
        -------
        str :
            A string representing the acreage from the property site.
        """
        
        pass

    @abstractmethod
    def get_year_built(self) -> str:
        """Return the year built from the source html.

        Returns
        -------
        str :
            A string representing the year built from the property site.
        """
        
        pass

    def execute(self) -> dict:
        """Get all of the supported attributes from the source html.
        
        Returns
        -------
        dict :
            A dictionary with key, value pairs of the attributes
            as scraped from the source html.
        """
        
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
        """Arrange the data following structures defined by streamlit.
        
        Parameters
        ----------
        dict :
            A dictionary with key, value pairs of the attributes
            as scraped from the source html.
        """
        
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
