

def format_string(key: str, value, is_attribute_correct: bool=None, with_color: bool=False):
    """Format the string for the report."""

    # NOTE :- WITH COLOR
    if with_color:
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
        
    # NOTE :- WITHOUT COLOR
    else:
        if key == 'price':
            return '${:,.2f}'.format(value)
        
        elif key == 'sqft':
            return '{value:,}'.format(value=value)
    
        else:
            return f'{value}'