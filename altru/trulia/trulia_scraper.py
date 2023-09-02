import re
from decimal import Decimal
import json
from altru.scraper.scraper import Scraper


test_data = {
    'address': '99 Fairfield Pond Ln,\xa0Sagaponack, NY 11963', 
    'price': '$18,995,000', 
    'bedrooms': '9', 
    'bathrooms': '15', 
    'sqft': '12,205', 
    'acre': '2.07 Acres', 
    'year_built': '2016'
}


class TruliaScraper(Scraper):

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
                # TODO: find a better way to do this that doesn't require using decimals
                data[key] = float(Decimal(re.sub(r'[^\d.]', '', value))) # must remove '$' and commas before casting to int

            elif key == 'bedrooms' or key == 'bathrooms':
                value = value.split(" ")[0]
                data[key] = int(value) # convert to correct type

            elif key == 'sqft':
                value = value.split(" ")[0]
                data[key] = int(value.replace(',', '')) # must remove commas before casting to int

            elif key == 'acre':
                data[key] = float(value) # Remove ' Acres' and cast to float

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
        street_address = self.soup.find('span', attrs={'data-testid': 'home-details-summary-headline'}).string
        county_state_zip = self.soup.find('span', attrs={'data-testid': 'home-details-summary-city-state'}).string
        return f'{street_address}, {county_state_zip}'

    def get_price(self) -> str:
        """Get the price from the source html.

        Returns
        -------
        str :
            A string representing the price from the property site.
        """

        parent = self.soup.find('h3', attrs={'data-testid': 'on-market-price-details'})
        # get the first child's text
        return parent.findChildren()[0].text


    def get_bedrooms(self) -> str:
        """Return the number of bedrooms from the source html.

        Returns
        -------
        str :
            A string representing the number of bedrooms from the
            property site.
        """

        bedBathItems = self.soup.find('div', attrs={'data-testid': 'home-summary-size-bedrooms'})
        # get the first child's text
        return bedBathItems.findChildren()[0].text

    def get_bathrooms(self) -> str:
        """Return the number of bathrooms from the source html.

        Returns
        -------
        str :
            A string representing the nubmer of bathrooms from the
            property site.
        """

        bedBathItems = self.soup.find('div', attrs={'data-testid': 'home-summary-size-bathrooms'})
        return bedBathItems.findChildren()[0].text


    def get_sqft(self) -> str:
        """Return the interior square footage from the source html.

        Returns
        -------
        str :
            A string representing the interior square footage from the
            property site.
        """

        bedBathItems = self.soup.find('div', attrs={'data-testid': 'home-summary-size-floorspace'})
        return bedBathItems.findChildren()[0].text
            
    def get_acre(self) -> str:
        """Return the acreage (lot size) from the source html.

        Returns
        -------
        str :
            A string representing the acreage from the property site.
        """

        # TODO: Implement this
        pattern = re.compile(r'Lot Area:') # returns `Lot Area: 2.07 acres`
        acre = self.soup.find(string=pattern)
        acre = re.sub(r'[^\d*.\d*]', '', acre)
        
        return acre

    def get_year_built(self) -> str:
        """Return the year built from the source html.

        Returns
        -------
        str :
            A string representing the year built from the property site.
        """

        # TODO: Implement this
        pattern = re.compile(r'Year Built:') # returns `Year Built: 2016`
        year_built = self.soup.find(string=pattern) 
        year_built = re.sub(r'[^\d{4}]', '', year_built)

        return year_built

if __name__=="__main__":
    scraper = TruliaScraper(
        api_key='f0bf7cd722f9d087a9ca5e358ff4df19',
        url='https://www.trulia.com/p/ny/sagaponack/99-fairfield-pond-ln-sagaponack-ny-11963--2184612195'
    )

    data = scraper.execute()

    print(json.dumps(data, indent=4))

    

    
