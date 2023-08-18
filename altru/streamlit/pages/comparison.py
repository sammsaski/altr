import streamlit as st
from difflib import Differ
import re

# NOTE: Add streamlit on-Hover tabs: https://github.com/Socvest/streamlit-on-Hover-tabs

true_data = {
    'address': '88 Rose Way, Bridgehampton, NY 11932',
    'price': '$21,000,000',
    'bedrooms': '10',
    'bathrooms': '15',
    'sqft': '12,300',
    'acre': '1.5 Acres',
    'year_built': '2022'
}

scraped_data = {
    'address': '88 Rose Way, Water Mills, NY 11976',
    'price': '$21,000,000',
    'bedrooms': '10',
    'bathrooms': '15',
    'sqft': '12,300',
    'acre': '1.50 Acres',
    'year_built': '2022'
}

st.title(f"Comparison Report for")
st.header(f":green[{true_data['address']}]")

st.divider()

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


# Difference

# NOTE: KEEP WORKING ON THIS.
# with st.container():
# same, d = compare_address(true_data['address'], scraped_data['address'])
wa, ra = compare_address(true_data['address'], scraped_data['address'])

attrs = ['address', 'price' , 'bedrooms', 'bathrooms', 'sqft', 'acre', 'year_built']

call_dict = {
    'address': compare_address,
    'price': compare_price,
    'bedrooms': compare_bedrooms,
    'bathrooms': compare_bathrooms,
    'sqft': compare_sqft,
    'acre': compare_acre,
    'year_built': compare_year_built,
}

for a in attrs:
    col = st.columns(2)
    w, r = call_dict[a](true_data[a], scraped_data[a])

    if a == 'address':
        col[0].metric(a, scraped_data[a])
        col[1].header(':green[correct]' if w == r else ':red[incorrect]')
    else:
        col[0].metric(a, w)
        col[1].header(r)

# st.subheader(wa)
# st.subheader(ra)

# st.divider()

# wp, rp = compare_price(true_data['price'], scraped_data['price'])
# p1, p2 = st.columns(2)
# p1 = st.write(wp)
# p2 = st.write(rp)

# st.divider()

# wb, rb = compare_bedrooms(true_data['bedrooms'], scraped_data['bedrooms'])
# st.subheader(wb)
# st.subheader(rb)

# st.divider()

# wba, rba = compare_bathrooms(true_data['bathrooms'], scraped_data['bathrooms'])
# st.subheader(wba)
# st.subheader(rba)

# st.divider()

# ws, rs = compare_sqft(true_data['sqft'], scraped_data['sqft'])
# st.subheader(ws)
# st.subheader(rs)

# st.divider()

# wac, rac = compare_acre(true_data['acre'], scraped_data['acre'])
# st.subheader(wac)
# st.subheader(rac)

# st.divider()

# wy, ry = compare_year_built(true_data['year_built'], scraped_data['year_built'])
# st.subheader(wy)
# st.subheader(ry)

