from fuzzywuzzy import fuzz


class PropertyComparison:
    """
    This class contains the methods necessary to compare different attributes of a property.

    For these comparisons, the goal is to take in two inputs and output a boolean denoting the whether or not
    the input strings are equivalent.
    """    

    # TODO: Add type annotations
    @staticmethod
    def equal(s, t):

        # Covers price, bedrooms, bathrooms, sqft, acre, year_built
        if (type(s) == type(t) == int) or (type(s) == type(t) == float):
            return s == t
        
        # Covers address
        # TODO: Need a better comparison tool for this. fuzzy string matching will work for the street address, but everything else will need to be exact.
        if type(s) == type(t) == str:
            return fuzz.token_sort_ratio(s, t) > 90
    