"""
Homes.com
"""

import re
from decimal import Decimal
import json
from altru.scraper.scraper import Scraper

"""
Expected behavior output from .execute() looks like:

        {
            "address": "99 Fairfield Pond Ln, Sagaponack, NY 11963,
            "price": "$18,995,000",
            "bedrooms": "9 Beds",
            "bathrooms": "15 Baths",
            "sqft": "12,205 sqft",
            "acre": "2.07",
            "year_built": "2016
        }
"""



test_data = {
    'address': '99 Fairfield Pond Ln,\xa0Sagaponack, NY 11963', 
    'price': '$18,995,000', 
    'bedrooms': '9', 
    'bathrooms': '15', 
    'sqft': '12,205', 
    'acre': '2.07 Acres', 
    'year_built': '2016'
}


class HomesScraper(Scraper):

    def __init__(self, api_key=None, url=None) -> None:
        super().__init__(api_key=api_key, url=url)

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

        data = {}

        for key, value in scraped_data.items():
            if key == 'address':
                # TODO: Convert address to its parts.
                pass

            elif key == 'price':
                data[key] = float(Decimal(re.sub(r'[^\d.]', '', value))) # must remove '$' and commas before casting to int

            elif key == 'bedrooms' or key == 'bathrooms':
                data[key] = int(value) # convert to correct type

            elif key == 'sqft':
                data[key] = int(value.replace(',', '')) # must remove commas before casting to int

            elif key == 'acre':
                data[key] = float(value)

            elif key == 'year_built':
                data[key] = int(value)

            else:
                raise Exception(f'An unexpected value (key: {key}) has entered the scraped data.')
            
        return data
    
    def get_address(self) -> str:
        """Get the address from the source html.

        Returns
        -------
        str :
            A string representing the address from the property site.
        """
        street_address = self.soup.find('h1').text.strip()

        county_state_zip = self.soup.find('span', attrs={'class': 'property-info-address-citystatezip'})
        county_state, zip_code = county_state_zip.findChildren()
        county_state = county_state.string
        zip_code = zip_code.string
        
        return f'{street_address}, {county_state} {zip_code}'

    def get_price(self) -> str:
        """Get the price from the source html.

        Returns
        -------
        str :
            A string representing the price from the property site.
        """

        return self.soup.find('span', attrs={'id': 'price'}).string

    def get_bedrooms(self) -> str:
        """Return the number of bedrooms from the source html.

        Returns
        -------
        str :
            A string representing the number of bedrooms from the
            property site.
        """

        bedBathItems = self.soup.find('span', attrs={'class': 'beds'})

        children = bedBathItems.findChildren()[0]
        return children.string

    def get_bathrooms(self) -> str:
        """Return the number of bathrooms from the source html.

        Returns
        -------
        str :
            A string representing the nubmer of bathrooms from the
            property site.
        """

        bedBathItems = self.soup.find('span', text=r'Baths')
        bedBathItems = bedBathItems.find_previous_siblings()[0]
        return bedBathItems.string

    def get_sqft(self) -> str:
        """Return the interior square footage from the source html.

        Returns
        -------
        str :
            A string representing the interior square footage from the
            property site.
        """

        element = self.soup.find('span', attrs={'class': 'sqft'})

        children = element.findChildren()[0]
        return children.string
            
    def get_acre(self) -> str:
        """Return the acreage (lot size) from the source html.

        Returns
        -------
        str :
            A string representing the acreage from the property site.
        """

        element = self.soup.find('span', attrs={'class': 'lotsize'})
        
        children = element.findChildren()[0]
        return children.string

    def get_year_built(self) -> str:
        """Return the year built from the source html.

        Returns
        -------
        str :
            A string representing the year built from the property site.
        """

        # element = self.soup.find_all('p', attrs={'class': 'home-facts-card-title'})
        # element = self.soup.find('p', text=r'Year Built*')
        element = self.soup.find('p', text=r'Year Built | Renovated')
        year_built_string = element.find_next_sibling().text

        return year_built_string.split(" ")[0]

if __name__=="__main__":
    scraper = HomesScraper(
        api_key='f0bf7cd722f9d087a9ca5e358ff4df19',
        url='https://www.homes.com/property/99-fairfield-pond-ln-sagaponack-ny/1nge7tnwj9czr/'
    )

    data = scraper.execute()

    print(json.dumps(data, indent=4))
