import os
from typing import List
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from altru.zillow.zillow_scraper import ZillowScraper
from altru.comparison.compare import PropertyComparison

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

        # for property in self.properties:
            # print(property.get().to_dict()) 
            # outputs: {'bathrooms': '15', 'bedrooms': '10', 'sqft': '15,000', 'price': '$21,000,000', 'acre': '1.50 Acres', 'address': '88 Rose Way, Water Mill, NY 11976', 'user': 'ssasaki', 'year_built': '2022'}
            # outputs: {'bathrooms': 15, 'bedrooms': 9, 'sqft': 10930, 'price': 18995000.0, 'acre': 2.07, 'address': '99 Fairfield Pond Lane, Sagaponack, NY 11962', 'user': 'ssasaki', 'year_built': 1995}
        # print(self.listing_sites) # outputs ['Zillow']
        # print(self.api_key) # outputs: f0bf7cd722f9d087a9ca5e358ff4df19

    def get_true_data(self, property) -> dict:
        """Retrieve the true data for one property.
        
        Return: 
            dict
        """
        return property.get().to_dict()

    # TODO: Add a feature to build/find the url based on the house properties.
    def get_scraped_data(self, scraper, url):
        """Retrieve the scraped data for one property."""
        scraper.request_html(api_key=self.api_key, url=url)
        return scraper.execute()

    # TODO: Add type annotations for the types of scrapers that are supported.
    def audit_properties(self, scraper):
        """Return a list of 
        """
        return [scraper.request_html(api_key=self.api_key, url=property['url']).execute() for property in self.properties]

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
                true_data = self.get_true_data(property)
                zillow = ZillowScraper()
                scraped_data = self.get_scraped_data(scraper=zillow, url=true_data['urls']['Zillow'])
                scraped_data = zillow.normalize_data(scraped_data=scraped_data)

                # TODO: Abstract this part out
                # perform the comparison while keeping track of accuracy stats
                is_property_correct = True
                property_result = {}
                for attr, scraped_value in scraped_data.items(): # we use scraped data because true_data has some additional attributes we don't want to check (like urls, username)
                    true_value = true_data[attr]
                    if PropertyComparison.equal(scraped_value, true_value):
                        property_result[attr] = f':green[{scraped_value}]'
                    else:
                        property_result[attr] = f':red[{scraped_value}]'
                        is_property_correct = False
                
                if is_property_correct:
                    correct += 1
                
                # we use `property_result` to build the visualization of the audit
                result[property] = property_result
        return result, correct, total
                

