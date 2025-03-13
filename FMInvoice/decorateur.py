from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def is_admin(user):
    return user.groups.filter(name='admin').exists()

def is_facturier(user):
    return user.groups.filter(name='facturier').exists()

def admin_required(view_func):
    return user_passes_test(is_admin, login_url='/access_denied/')(view_func)

def facturier_required(view_func):
    return user_passes_test(is_facturier, login_url='/access_denied/')(view_func)