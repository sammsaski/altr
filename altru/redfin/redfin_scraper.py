import re
from decimal import Decimal
from altru.scraper.scraper import Scraper


# NOTE: Incomplete.

test_data = {
    'address': '99 Fairfield Pond Ln,\xa0Sagaponack, NY 11963', 
    'price': '$18,995,000', 
    'bedrooms': '9', 
    'bathrooms': '15', 
    'sqft': '12,205', 
    'acre': '2.07 Acres', 
    'year_built': '2016'
}


class RedfinScraper(Scraper):

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
        """Get the address from the source html.

        Returns
        -------
        str :
            A string representing the address from the property site.
        """
        parent = self.soup.find('h1')
        return parent.text

    def get_price(self) -> str:
        """Get the price from the source html.

        Returns
        -------
        str :
            A string representing the price from the property site.
        """

        parent = self.soup.find('span', attrs={'data-testid': 'price'})
        children = parent.findChildren()
        
        return str(children[0].string)


    def get_bedrooms(self) -> str:
        """Return the number of bedrooms from the source html.

        Returns
        -------
        str :
            A string representing the number of bedrooms from the
            property site.
        """

        bedBathItems = self.soup.find_all('span', attrs={'data-testid': 'bed-bath-item'})

        for item in bedBathItems:
            children = item.findChildren()
            value = children[0].string
            unit = children[1].text.strip()

            if 'bd' == unit:
                return str(value)

    def get_bathrooms(self) -> str:
        """Return the number of bathrooms from the source html.

        Returns
        -------
        str :
            A string representing the nubmer of bathrooms from the
            property site.
        """

        bedBathItems = self.soup.find_all('span', attrs={'data-testid': 'bed-bath-item'})

        for item in bedBathItems:
            children = item.findChildren()
            value = children[0].string
            unit = children[1].text.strip()

            if 'ba' == unit:
                return str(value)

    def get_sqft(self) -> str:
        """Return the interior square footage from the source html.

        Returns
        -------
        str :
            A string representing the interior square footage from the
            property site.
        """

        bedBathItems = self.soup.find_all('span', attrs={'data-testid': 'bed-bath-item'})

        for item in bedBathItems:
            children = item.findChildren()
            value = children[0].string
            unit = children[1].text.strip()

            if 'sqft' == unit:
                return str(value)
            
    def get_acre(self) -> str:
        """Return the acreage (lot size) from the source html.

        Returns
        -------
        str :
            A string representing the acreage from the property site.
        """

        element = self.soup.find('span', text=re.compile(r'\d*\.\d* Acres?'))
        return str(element.string)

    def get_year_built(self) -> str:
        """Return the year built from the source html.

        Returns
        -------
        str :
            A string representing the year built from the property site.
        """

        element = self.soup.find('span', text=re.compile(r'Built in \d\d\d\d'))
        return element.string[9:]

if __name__=="__main__":
    scraper = RedfinScraper()

    results = scraper.normalize_data(scraped_data=test_data)
    print(results)
