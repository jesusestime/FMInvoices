from django.urls import path


from FMInvoice.views import (
    register_view,
    login_view,
    user_view,
    logout_view,
    profile_update_view,
    user_activation_view,
    password_change_view,
    index
)
urlpatterns = [

    # Home Page
    path("", index, name="index"),

    # User Authentication
    path("user/register/", register_view, name="user_register"),
    path("user/login/", login_view, name="user_login"),
    path("user/logout/", logout_view, name="user_logout"),

    # Profile Management
    path("user/profile/update/", profile_update_view, name="user_update_profile"),

    # User profile View
    path("user/profile/view/",user_view, name="user_view"),

    # User Activation (Admin)
    path("user/activate/<int:user_id>/", user_activation_view, name="user_activation"),

    # Password Change (Logged-in Users)
    path("user/password/change/", password_change_view, name="user_password_change"),



]