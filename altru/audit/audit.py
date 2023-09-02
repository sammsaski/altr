import os
from typing import List, Dict, Tuple
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from altru.zillow.zillow_scraper import ZillowScraper
from altru.comparison.compare import PropertyComparison
from altru.audit.display_data import format_string

def normalize_db_data(data: dict) -> dict:
    """Normalize the requested database data to data types of:
        'address': str
        'price': int
        'bedrooms': int
        'bathrooms': int
        'sqft': int
        'acre': float
        'year_built': int

    Parameters
    ----------
    data : dict
        The data requested from the database.

    Returns
    -------
    dict
        The data type cast to the types defined above.
    """
    
    KEYS = ['address', 'price', 'bedrooms', 'bathrooms', 'sqft', 'acre', 'year_built']
    
    for key in KEYS:
        value = data[key]
        if key == 'address':
            data[key] = str(value)
        elif key == 'acre':
            data[key] = float(value)
        else:
            data[key] = int(value)
    return data

class Audit:

    """For the audit, we need to be able to:
    
    1. Take in some specifications for the audit (properties, listing_sites)
    2. Perform the audit (scraping the data from each listing site and running comparison)
        i.   scrape the data for each property
        ii.  get the true data for each property
        iii. run comparison between the true and scraped data
    3. Display the audit.
    4. Keep a history of the audit.
    
    """

    # TODO: Think about how to get the URLs for the properties.

    # TODO: Add better type annotations.
    def __init__(self, properties: list, listing_sites: list, api_key: str):
        """Instantiates an audit with the properties and listing sites to audit along with
        the api key to use when scraping the data.

        properties: List[DocumentReference]
        listing_sites: List[str]
        api_key: str
        """
        self.properties = properties
        self.listing_sites = listing_sites
        self.api_key = api_key

    def get_true_data(self, property) -> dict:
        """Retrieve the true data for one property.
        
        Returns
        -------
        dict :
            A dictionary with the true data retrieved from the database.
        """
        return property.get().to_dict()

    # TODO: Add a feature to build/find the url based on the house properties.
    def get_scraped_data(self, scraper, url):
        """Retrieve the scraped data for one property."""
        scraper.request_html(api_key=self.api_key, url=url)
        return scraper.execute()
    
    def format_string(self, key: str, value, is_attribute_correct: bool):
        """Format the string for the report."""
        if key == 'address':
            return ':{color}[{value}]'.format(color='green' if is_attribute_correct else 'red', value=value)

        elif key == 'price':
            value = '${:,.2f}'.format(value)
            return ':{color}[{value}]'.format(color='green' if is_attribute_correct else 'red', value=value)

        elif key == 'sqft':
            value = '{value:,}'.format(value=value)
            return ':{color}[{value}]'.format(color='green' if is_attribute_correct else 'red', value=value)
        
        # if key == 'bedrooms' or key == 'bathrooms' or key == 'acre' or key == 'year_built':
        else:
            return ':{color}[{value}]'.format(color='green' if is_attribute_correct else 'red', value=value)

    # TODO: Add type annotations for the types of scrapers that are supported.
    def audit_properties(self, scraper):
        """Return a list of 
        """
        return [scraper.request_html(api_key=self.api_key, url=property['url']).execute() for property in self.properties]

    # TODO: Add type annotations.
    def execute(self):
        """Execute the audit."""
        total = len(self.properties)
        correct = 0

        # TODO: Add support for statistics like 'how many properties had their addresses correct?' i.e. get more specific with stats.
        
        result = {}
        for listing_site in self.listing_sites:
            if listing_site == 'Zillow': # TODO: Implement work for multiple listing sites.
                pass

            for property in self.properties:
                
                # get the scraped and true data
                true_data = normalize_db_data(self.get_true_data(property))
                zillow = ZillowScraper()
                scraped_data = zillow.normalize_data(
                    scraped_data=self.get_scraped_data(scraper=zillow, url=true_data['urls']['Zillow'])
                )

                property_result, is_property_correct = PropertyComparison.compare(scraped_data, true_data)
                
                if is_property_correct:
                    correct += 1
                
                # we use `property_result` to build the visualization of the audit
                result[property] = property_result
        return result, correct, total
                
if __name__=='__main__':
    # test get_true_data method
    db = firestore.Client.from_service_account_json(os.getcwd() + '/firestore-key.json')

    properties = db.collection('audits').document('Qc6sInDWS18iQcSr2NGw').get().to_dict()['properties']

    audit = Audit(properties=properties, listing_sites=['Zillow'], api_key='')
    
    for property in properties:
        true_data = audit.get_true_data(property=property)
        print(true_data)
        true_data = normalize_db_data(true_data)
        print(true_data)

