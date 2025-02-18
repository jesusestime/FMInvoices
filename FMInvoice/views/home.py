from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
# Function to view home page
def index(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'FMInvoice/home/index.html'
    )


# Display a view for after redirecting the new employee without is_staff or is_superuser roles
def perm_is_employee(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'FMInvoice/perm/employee.html'
    )


# Display a view for after redirecting the employee without is_superuser role
def perm_is_admin(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'FMInvoice/perm/admin.html'
    )