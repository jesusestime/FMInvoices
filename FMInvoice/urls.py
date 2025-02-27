from django.urls import path

from FMInvoice.models import UtilisateurEmetteurStation
from FMInvoice.views import (
    register_view,
    login_view,
    user_view,
    logout_view,
    profile_update_view,
    user_activation_view,
    password_change_view,user_list_view,
    StationRadioDepartementview, UtilisateurEmetteurStationview,home,Clientview,Emetteurview,CategorieEmissionServiceView,EmissionView,ServiceView
)

urlpatterns = [

    # Home Page
    path("", home.index, name="index"),
    # User Authentication
    path("user/register/", register_view, name="user_register"),
    path("user/login/", login_view, name="user_login"),
    path("user/logout/", logout_view, name="user_logout"),
    path("user/list/",user_list_view, name="user_list"),
    # Profile Management
    path("user/profile/update/", profile_update_view, name="user_update_profile"),
    # User profile View
    path("user/profile/view/",user_view, name="user_view"),
    # User Activation (Admin)
    path("user/activate/<int:user_id>/", user_activation_view, name="user_activation"),
    # Password Change (Logged-in Users)
    path("user/password/change/", password_change_view, name="user_password_change"),



    # Station Radio Departement URLs
    path("station_radio_departement/", StationRadioDepartementview.index, name='station_radio_departement_index'),
    path("station_radio_departement/create/", StationRadioDepartementview.create, name='station_radio_departement_create'),
    path("station_radio_departement/edit/<int:id>/", StationRadioDepartementview.edit,
         name='station_radio_departement_edit'),
    path("station_radio_departement/delete/<int:id>/", StationRadioDepartementview.delete,
         name='station_radio_departement_delete'),


    path("utilisateur_emetteur_station/", UtilisateurEmetteurStationview.index, name='utilisateur_emetteur_index'),
    path("utilisateur_emetteur_station/create/", UtilisateurEmetteurStationview.create,
         name='utilisateur_emetteur_create'),
    path("utilisateur_emetteur_station/edit/<int:id>/", UtilisateurEmetteurStationview.edit,
         name='utilisateur_emetteur_edit'),
    path("utilisateur_emetteur_station/delete/<int:id>/", UtilisateurEmetteurStationview.delete,
         name='utilisateur_emetteur_delete'),



    path("client/", Clientview.index, name='client_index'),
    path("client/create/", Clientview.create, name='client_create'),
    path("client/edit/<int:id>/", Clientview.edit, name='client_edit'),
    path("client/delete/<int:id>/", Clientview.delete, name='client_delete'),
    path("client/detail/<int:id>/", Clientview.client_detail, name='client_detail'),



    path('emetteur/', Emetteurview.emetteur_index, name='emetteur_index'),
    path('emetteur/create/', Emetteurview.emetteur_create, name='emetteur_create'),
    path('emetteur/edit/<int:id>/', Emetteurview.emetteur_edit, name='emetteur_edit'),
    path('emetteur/delete/<int:id>/', Emetteurview.emetteur_delete, name='emetteur_delete'),
    path('emetteur/detail/<int:id>/', Emetteurview.emetteur_detail, name='emetteur_detail'),



    path("categorie_emission_service/", CategorieEmissionServiceView.index, name='categorie_emission_service_index'),
    path("categorie_emission_service/create/", CategorieEmissionServiceView.create,
         name='categorie_emission_service_create'),
    path("categorie_emission_service/edit/<int:id>/", CategorieEmissionServiceView.edit,
         name='categorie_emission_service_edit'),
    path("categorie_emission_service/delete/<int:id>/", CategorieEmissionServiceView.delete,
         name='categorie_emission_service_delete'),

    path("emission/", EmissionView.emission_index, name='emission_index'),
    path("emission/create/", EmissionView.emission_create, name='emission_create'),
    path("emission/edit/<int:id>/", EmissionView.emission_edit, name='emission_edit'),
    path("emission/delete/<int:id>/", EmissionView.emission_delete, name='emission_delete'),



    path("service/", ServiceView.service_index, name='service_index'),
    path("service/create/", ServiceView.service_create, name='service_create'),
    path("service/edit/<int:id>/", ServiceView.service_edit, name='service_edit'),
    path("service/delete/<int:id>/", ServiceView.service_delete, name='service_delete'),
]