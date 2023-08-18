import streamlit as st
from difflib import Differ
import re

st.title("Comparison")

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

true, scraped = st.columns(2)

# Two columns
with true:
    for key, value in true_data.items():
        st.metric(key, value)

with scraped:
    for key, value in scraped_data.items():
        st.metric(key, value)


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
    d = Differ()

    t = re.sub('[^0-9]','', t)
    s = re.sub('[^0-9]','', s)

    wrong = ''
    right = ''

    if int(t) == int(s):

        s = '{:,}'.format(int(s))
        t = '{:,}'.format(int(t))

        wrong = f':green[${s}]'
        right = f':green[${t}]'
    
    # NOTE: Add the else case.
    
    return wrong, right


def compare_bedrooms(t, s):
    d = Differ()

    # NOTE: Finish this.
    

# Difference

# NOTE: KEEP WORKING ON THIS.
with st.container():
    # same, d = compare_address(true_data['address'], scraped_data['address'])
    wa, ra = compare_address(true_data['address'], scraped_data['address'])

    st.subheader(wa)
    st.subheader(ra)

    st.divider()

    wp, rp = compare_price(true_data['price'], scraped_data['price'])
    st.subheader(wp)
    st.subheader(rp)

    st.divider()

    wb, rb = compare_bedrooms(true_data['bedrooms'], scraped_data['bedrooms'])
    st.subheader(wb)
    st.subheader(rb)


