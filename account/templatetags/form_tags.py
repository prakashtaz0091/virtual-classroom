# account/templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})

# """
# <input class="w-full px-3 py-2 border rounded mb-4" type='text' placeholder='Enter your username' />

# """
