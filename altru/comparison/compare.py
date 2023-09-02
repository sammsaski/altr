from fuzzywuzzy import fuzz
from typing import Any, Tuple

class PropertyComparison:
    """
    Support the audit by comparing different attributes of a property.

    Additionally, support formatting the strings used to build the
    audit report that will be displayed by streamlit.
    """    

    # TODO: Add type annotations
    @staticmethod
    def _equal(s: Any, t: Any) -> bool:
        """Check the equality of the scraped (s) and true (t) data.
        
        Parameters
        ----------
        s : Any
            The scraped data.
        t : Any
            The true data.

        Returns
        -------
        bool :
            Whether or not the scraped and true data are equal.
        """
        
        # Covers address
        # TODO: Need a better comparison tool for this. fuzzy string matching will work for the street address, but everything else will need to be exact.
        if type(s) == type(t) == str:
            return fuzz.token_sort_ratio(s, t) > 90
        
        # Covers price, bedrooms, bathrooms, sqft, acre, year_built
        return s == t
    
    @staticmethod
    def format_string(key: str, value: Any, is_attribute_correct: bool) -> str:
        """Format the string for the report.
        
        Parameters
        ----------
        key : str
            The key corresponding to the desired value in the data.
        value : Any
            The value associated with the key from the data.
        is_attribute_correct : bool
            Whether or not the scraped attribute associated with the
            key, value pair was accurate compared to the true data.

        Returns
        -------
        str :
            A string formatted for use by streamlit in the audit report.
        """

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
    
    @staticmethod
    def compare(s: dict, t: dict) -> Tuple[dict, bool]:
        """Compare the attributes of scraped and true data.
        
        Parameters
        ----------
        s : dict
            The scraped data.
        t : dict
            The true data.
        
        Returns
        -------
        dict :
            A dictionary containing the scraped data formatted for
            use by streamlit in the audit report.
        bool :
            If the scraped data was equal to the trued data or not.
        """
        
        is_property_correct = True
        property_result = {}

        # we use scraped data because true_data has some additional attributes we don't want to check (like urls, username)
        for attr, scraped_value in s.items():
            true_value = t[attr]
            is_attribute_correct = PropertyComparison._equal(scraped_value, true_value)
            property_result[attr] = PropertyComparison.format_string(key=attr, value=scraped_value, is_attribute_correct=is_attribute_correct) #with_color=True
            is_property_correct = (is_property_correct and is_attribute_correct)

        return property_result, is_property_correct