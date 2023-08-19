import streamlit as st
from difflib import Differ
import re
import streamlit.components.v1 as components
from altru.comparison.compare import PropertyComparison as pc

# TODO: Add streamlit on-Hover tabs: https://github.com/Socvest/streamlit-on-Hover-tabs


#-----------------------#
#------ TESTING --------#
#-----------------------#
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


#-------------------------#
#-------- METHODS --------#
#-------------------------#
ATTRS = ['address', 'price' , 'bedrooms', 'bathrooms', 'sqft', 'acre', 'year_built']


def color_string(s: str, t: str, eq) -> str:
    """Color the string based on accuracy.
    
    s (str)   : the scraped data.
    t (str)   : the true data.
    eq (bool) : whether or not the scraped and true data are equivalent.

    Returns:
        str : the scraped data colored accordingly (red for incorrect, green for correct).
    """
    return f':green[{s}]' if eq else f':red[{s}]'

def perform_comparison(sd: dict, td: dict) -> dict:
    """Perform the comparison of the following attributes of a property.
    [ address, price, bedrooms, bathrooms, sqft, acreage, year built ].

    sd (dict) : key, value pairs of the scraped data for a property.
    td (dict) : key, value pairs of the true data for a property.

    Returns:
        (dict) : key, value pairs of the colored strings for building the report.
    """

    report = {'correct': 0, 'total': 0}

    for a in ATTRS:

        if a == 'address':
            eq = pc.compare_comma_separated_string(sd[a], td[a])
            if eq:
                report['correct'] += 1

            # build the string
            s = sd[a].split(", ")
            s[2], temp = s[2].split(" ")
            s.append(temp)

            t = td[a].split(", ")
            t[2], temp = t[2].split(" ")
            t.append(temp)

            s = [color_string(x, y, eq=(x == y)) for x, y in zip(s, t)]
            report['address'] = f'{s[0]}, {s[1]}, {s[2]} {s[3]}'
            report['total'] += 1


        if a == 'price':
            eq = pc.compare_price(sd[a], td[a])
            if eq:
                report['correct'] += 1
            
            # build the string
            report[a] = color_string(sd[a], td[a], eq=eq)
            report['total'] += 1

        if a == 'bedrooms':
            eq = (sd[a] == td[a])
            if eq:
                report['correct'] += 1
            
            # build the string
            report[a] = color_string(sd[a], td[a], eq=eq)
            report['total'] += 1

        if a == 'bathrooms':
            eq = (sd[a] == td[a])
            if eq:
                report['correct'] += 1
            
            # build the string
            report[a] = color_string(sd[a], td[a], eq=eq)
            report['total'] += 1
        
        if a == 'sqft':
            eq = (sd[a] == td[a])
            if eq:
                report['correct'] += 1
            
            # build the string
            report[a] = color_string(sd[a], td[a], eq=eq)
            report['total'] += 1

        if a == 'acre':
            eq = pc.compare_float_string(sd[a], td[a])
            if eq:
                report['correct'] += 1
            
            # build the string
            report[a] = color_string(sd[a], td[a], eq=eq)
            report['total'] += 1

        if a == 'year_built':
            eq = (sd[a] == td[a])
            if eq:
                report['correct'] += 1
            
            # build the string
            report[a] = color_string(sd[a], td[a], eq=eq)
            report['total'] += 1

    return report

#-------------------------#
#-------- STRUCTURE ------#
#-------------------------#

# NOTE :- adding style to align the labels in the comparison report.
css = '''
    [data-testid="stCaptionContainer"] {
        padding-top: 15px;
    }
'''

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# red : rgb(255, 75, 75);
# green : rgb(61, 213, 109);

# TITLE
st.subheader(f"Comparison Report for")
st.header(f":green[{true_data['address']}]")

st.divider()


# BUILD THE COMPARISON REPORT

comparison = perform_comparison(scraped_data, true_data)

for key, value in comparison.items():
    if key in ATTRS:
        if key == 'address':
            col = st.columns([3, 14])
            col[0].caption(key)
            col[1].subheader(value)
        else:
            col = st.columns([3, 6, 2, 6])
            col[0].caption(key)
            col[1].subheader(true_data[key])
            col[2].subheader('▸')
            col[3].subheader(value)

st.divider()

# STATISTICS
st.subheader('Analytics')
col = st.columns(3)
col[0].metric('accuracy', '{:.2f}'.format(comparison.get('correct') / comparison.get('total') * 100) + '%')
col[1].metric('correct', comparison.get('correct'))
col[2].metric('total', comparison.get('total'))
