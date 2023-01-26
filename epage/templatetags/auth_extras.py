from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='is_admin')
def is_admin(user): 
    if user.is_superuser:
        return True
    group = Group.objects.get(name='Administrator') 
    return True if group in user.groups.all() else False