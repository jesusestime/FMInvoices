from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from FMInvoice.forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    UserActivationForm,
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
)
from django.contrib.auth.models import User



def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("index")
        else:
            messages.error(request, "There was an error in the registration form. Please check the details.")
    else:
        form = CustomUserCreationForm()

    return render(request, "FMInvoice/accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = CustomAuthenticationForm()

    return render(request, "FMInvoice/accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Logout successful!')
    return redirect('user_login')


@login_required
def password_change_view(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, "Password changed successfully!")
            return redirect("user_view")
        else:
            messages.error(request, "There was an error changing your password. Please check the form.")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "FMInvoice/accounts/password_change.html", {"form": form})




@login_required
def user_activation_view(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect("index")

    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = UserActivationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User activation updated.")
            return redirect("user_list")
        else:
            messages.error(request, "Error updating user activation. Please try again.")
    else:
        form = UserActivationForm(instance=user)

    return render(request, "FMInvoice/accounts/activate.html", {"form": form, "user": user})



@login_required
def user_view(request):
    assert isinstance(request, HttpRequest)
    user_id = request.GET.get('id')  # Get id from query parameter

    if user_id is None or user_id == "":  # Check if id is provided
        employee = request.user
    else:
        try:
            user_id = int(user_id) # Convert to integer
            employee = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # Handle the case where the user with that ID doesn't exist.
            # You might want to return a 404, redirect, or display an error message.
            return HttpResponse("User not found", status=404)
        except ValueError: # Handle if user_id is not a valid integer
            return HttpResponse("Invalid user ID", status=400)



    return render(
        request,
        'FMInvoice/accounts/view.html',
        {
            'user': employee
        }
    )



# Profile Update
@login_required
def profile_update_view(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("user_view")
        else:
            messages.error(request, "There was an error updating your profile. Please check the form.")
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, "FMInvoice/accounts/edit.html", {"form": form})




@login_required
def user_list_view(request):
    users = User.objects.all().order_by('id')

    return render(request, "FMInvoice/accounts/index.html", {"users": users})
