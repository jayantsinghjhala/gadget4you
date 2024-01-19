from django import template
import locale
register = template.Library()

@register.filter
def calculate_discount_percentage(selling_price, discounted_price):
    try:
        selling_price = float(selling_price)
        discounted_price = float(discounted_price)
        discount_percentage = int((selling_price - discounted_price) / selling_price * 100)
        return f"{discount_percentage}%"
    except (TypeError, ValueError, ZeroDivisionError):
        return "Invalid input"

@register.filter
def replace_dash_with_br(value):
    words = value.split()
    modified_description = []

    for word in words:
        if word == '-':
            modified_description.append('<br>&nbsp;&nbsp;&nbsp;-')
        else:
            modified_description.append(word)

    return ' '.join(modified_description)

@register.filter
def format_indian(value):
    try:
        current_locale = locale.getlocale(locale.LC_NUMERIC)  # Get the current locale settings

        # Temporarily set locale to 'en_IN' to ensure integer output
        locale.setlocale(locale.LC_NUMERIC, 'en_IN')

        # Format the value using the updated locale settings
        formatted_value = locale.format_string("%d", value, grouping=True)

        # Revert back to the original locale settings
        locale.setlocale(locale.LC_NUMERIC, current_locale)

        return '₹'+formatted_value

    except (ValueError, locale.Error):
        return '₹'+str(value)

# @register.filter()
# def multiply(value, arg):
#     try:
#         return value * arg
#     except (ValueError, TypeError):
#         return value