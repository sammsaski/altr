from difflib import Differ
import re


class PropertyComparison:
    """
    This class contains the methods necessary to compare different attributes of a property.

    Some irregular behavior that needs to be implemented include:
    - comparison of comma separated strings (address)
    - comparison of a string with a $ in it (price)
    - comparison of floats within strings (acreage)

    For these comparisons, the goal is to take in two inputs and output a boolean denoting the whether or not
    the input strings are equivalent.
    """    

    # NOTE: For now, this works under the format : <street>, <county>, <state> <zip>
    def compare_comma_separated_string(s: str, t: str) -> bool:
        """Compare the components of a comma separated string.

        s (str) : the scraped data.
        t (str) : the true data.

        returns (bool) : whether or not the scraped and true data are equivalent.
        """
        return s.split(", ") == t.split(", ")
    
    def compare_dollar_amount(s: str, t: str) -> bool:
        """Check the equality of two dollar amounts.
        
        s (str) : the scraped data
        t (str) : the true data

        returns (bool) : whether or not the scraped and true data are equivalent.
        """
        temp_t = re.sub('[^0-9]','', t)
        temp_s = re.sub('[^0-9]','', s)

        eq = int(temp_t) == int(temp_s)

        return (s, f':green[{t}]') if eq else (f':red[{s}]', t)

    # NOTE: For now, this works under the format : <float value> <unit>
    def compare_float_string(s: str, t: str) -> bool:
        """Compare the components of a string containing a floating point value.
        
        s (str) : the scraped data.
        t (str) : the true data.

        returns (bool) : whether or not the scraped and true data are equivalent.
        """
        s = s.split(" ")
        t = t.split(" ")
    
        # NOTE: Add support for conversion.

        # unpack by value and unit
        sv, su = s
        tv, tu = t

        # Handles the case where one is 'acres' and the other is 'acre'.
        if (su in tu) or (tu in su):
            return float(sv) == float(tv)
        else:
            # NOTE: Need to do.
            pass 


    def compare_address(t, s):
        if t == s:
            return True, []
        
        # len of t and s should be the same after split.
        t = t.split(",")
        s = s.split(",")

        d = Differ()

        differences = [list(d.compare(x, y)) for x, y in zip(t, s)]

        wrong = ''
        right = ''

        for i, diff in enumerate(differences):

            diff = list(map(str.strip, diff))
            diff = list(map(lambda x: x.replace('', ' ') if x == '' else x, diff))

            if t[i] == ''.join(diff):
                wrong += f'{t[i]}, '
                right += f'{t[i]}, '
            else:
                wrong += f':red[{s[i]}], '
                right += f':green[{t[i]}], '
        
        return wrong[:-2], right[:-2]

    # NOTE: rename 'wrong' and 'right' variables. it is misleading.
    def compare_price(t, s):
        """
        """
        temp_t = re.sub('[^0-9]','', t)
        temp_s = re.sub('[^0-9]','', s)

        eq = int(temp_t) == int(temp_s)

        return (s, f':green[{t}]') if eq else (f':red[{s}]', t)

        


    # NOTE: Add type annotations
    # NOTE: Maybe add a better name. This doesn't exactly highlight what is happening.
    def compare_bedrooms(t: str, s: str):
        """Return colored strings based on the evaluation of the comparison between
        both the true and scraped input data.

        This method expects that the inputs can be directly type cast to 'int'.
        """
        return (s, f':green[{t}]') if int(s) == int(t) else (f':red[{s}]', t)
        

    # NOTE: Add type annotations
    # NOTE: Maybe add a better name. This doesn't exactly highlight what is happening.
    def compare_bathrooms(t: str, s: str):
        """Return colored strings based on the evaluation of the comparison between
        both the true and scraped input data.

        This method expects that the inputs can be directly type cast to 'int'.
        """
        return (s, f':green[{t}]') if int(s) == int(t) else (f':red[{s}]', t)
        
    def compare_sqft(t: str, s: str):
        t = re.sub('[^0-9]','', t)
        s = re.sub('[^0-9]','', s)

        # check equality
        eq = int(s) == int(t)

        s = '{:,}'.format(int(s))
        t = '{:,}'.format(int(t))

        return (s, f':green[{t}]') if eq else (f':red[{s}]', t)

    def compare_acre(t: str, s: str):
        temp_t = t.split(" ")
        temp_s = s.split(" ")

        # check equality
        eq = float(temp_t[0]) == float(temp_s[0])

        return (s, f':green[{t}]') if eq else (f':red[{s}]', t)
        
    def compare_year_built(t: str, s: str):
        return (s, f':green[{t}]') if int(s) == int(t) else (f':red[{s}]', t)
