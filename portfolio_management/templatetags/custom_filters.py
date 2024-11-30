from django import template

register = template.Library()

@register.filter
def format_symbol(value):
    """Replace underscores with empty space and convert to uppercase."""
    return value.replace('_', '').upper()
