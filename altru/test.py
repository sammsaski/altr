
from zillow.zillow_scraper import ZillowScraper

def test_sequence(url):
    zs = ZillowScraper(url=url)
    address = zs.get_address()
    print(address)

    print('-----------------------------------------')

    price = zs.get_price()
    print(f'Price: {price}')

    bedrooms = zs.get_bedrooms()
    print(f'Bedrooms: {bedrooms}')

    bathrooms = zs.get_bathrooms()
    print(f'Bathrooms: {bathrooms}')

    sqft = zs.get_sqft()
    print(f'Sqft: {sqft}')

    acre = zs.get_acre()
    print(f'Acre: {acre}')

    yb = zs.get_year_built()
    print(f'Year Built: {yb}')


if __name__=="__main__":
    print('\n')

    # 1. 88 Rose Way, Water Mill, NY 11976
    test_sequence(url="https://www.zillow.com/homes/88-Rose-Way-Water-Mill,-NY-11976_rb/32731171_zpid/")

    print('\n\n')

    # 2. 99 Fairfield Pond Lane, Sagaponack, NY 11963
    test_sequence(url="https://www.zillow.com/homes/99-Fairfield-Pond-Ln-Sagaponack,-NY-11963_rb/248847986_zpid/")

    print('\n')