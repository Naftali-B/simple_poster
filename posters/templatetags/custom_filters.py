from django import template

register = template.Library()

@register.filter
def first_word(value):
    """Returns the first word of the string."""
    return value.split()[0] if value else ''

@register.filter
def second_word(value):
    """Returns the second word of the string."""
    words = value.split()
    return words[1] if len(words) > 1 else ''

@register.filter
def rest_of_title(value):
    """Returns the rest of the title after the first two words."""
    words = value.split()
    return ' '.join(words[2:]) if len(words) > 2 else ''
