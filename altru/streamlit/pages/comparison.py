import streamlit as st
from difflib import Differ

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

def comparison(t, s):
    """Add type annotations"""
    if t == s:
        return True, []
    d = Differ()
    return False, list(d.compare(t, s))


# Difference

# NOTE: KEEP WORKING ON THIS.
with st.container():
    same, d = comparison(true_data['address'], scraped_data['address'])

    wrong = ''
    right = ''

    for x in d:
        if x[0] == ' ':
            wrong += x[2]
            right += x[2]
        elif x[0] == '+':
            right += f':green[{x[2]}]'
        else:
            wrong += f':red[{x[2]}]'
    
    st.markdown(wrong)
    st.markdown(right)
