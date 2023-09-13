import re
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


class ZillowScraper(Scraper):

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
                data[key] = int(re.sub(r'[^\d.]', '', value)) # must remove '$' and commas before casting to int

            elif key == 'bedrooms' or key == 'bathrooms':
                data[key] = int(value) # convert to correct type

            elif key == 'sqft':
                data[key] = int(scraped_data[key].replace(',', '')) # must remove commas before casting to int

            elif key == 'acre':
                data[key] = float(re.sub(r'[^\d*.\d*]', '', value).strip()) # Remove ' Acres' and cast to float

            elif key == 'year_built':
                data[key] = int(value)

            else:
                raise Exception(f'An unexpected value (key: {key}) has entered the scraped data.')
            
        return data
    
    def get_address(self) -> str:
        """Get the address from the source html.

        NOTE: Unique to the address is that it is an 'h1' element, which makes things easy.

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

        Because bedrooms is structured like multiple other attributes of the house, we have to check
        specifics about how the bedrooms are listed. Hence, we know that the children as referred to 
        by the code consists of 2--the value and the unit.

        Returns
        -------
        str :
            A string representing the number of bedrooms from the
            property site. NOTE: Only the number i.e. if listed 
            as `4 bd`, then return `4`.
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
            property site. NOTE: Only the number i.e. if listed 
            as `4 ba`, then return `4`.
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
            property site. NOTE: Only the number i.e. if listed 
            as `10,000 sqft`, then return `10,000`.
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

        NOTE: Finding an element in bs4 based on the text in the tag i.e. <p>Hello</p> trying to find the element with "Hello".

        Returns
        -------
        str :
            A string representing the acreage from the property site.
            NOTE: Only the number i.e. if listed as `0.99 Acres`, then 
            return `0.99`.
        """
        element = self.soup.find('span', text=re.compile(r'\d+(\.\d+)? Acres?'))
        return str(element.string)

    def get_year_built(self) -> str:
        """Return the year built from the source html.

        NOTE: Finding an element in bs4 based on the text in the tag i.e. <p>Hello</p> trying to find the element with "Hello".

        Returns
        -------
        str :
            A string representing the year built from the property site.
            NOTE: Only the year i.e. if listed as `Built in 1999`, then 
            return `1999`.
        """
        element = self.soup.find('span', text=re.compile(r'Built in \d\d\d\d'))
        return element.string[9:]

if __name__=="__main__":
    url1 = 'https://www.zillow.com/homedetails/335-Town-Ln-Amagansett-NY-11930/32662806_zpid/'
    url2 = 'https://www.zillow.com/homedetails/397-Sagg-Main-St-Sagaponack-NY-11962/2068763469_zpid/'

    api_key = 'api_key_placeholder'

    scraper = ZillowScraper(api_key=api_key, url=url1)
    results = scraper.get_acre()

    print(results)


