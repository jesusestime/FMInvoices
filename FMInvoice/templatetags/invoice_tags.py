# FMInvoice/templatetags/invoice_tags.py
from django import template

register = template.Library()

@register.filter
def has_admin_permission(user):
    # Check if user is in the "admin" group
    return user.is_authenticated and user.groups.filter(name='admin').exists()

@register.filter
def has_facturier_permission(user):
    # Placeholder: Check if user is in the "Facturier" group (adjust based on facturier_required)
    return user.is_authenticated and user.groups.filter(name='facturier').exists()