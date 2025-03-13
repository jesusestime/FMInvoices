from django.urls import path
from FMInvoice.decorateur import admin_required, facturier_required
from FMInvoice.models import UtilisateurEmetteurStation
from FMInvoice.views import (
    register_view,
    login_view,
    user_view,
    logout_view,
    profile_update_view,
    user_activation_view,
    password_change_view,user_list_view,
    StationRadioDepartementview, UtilisateurEmetteurStationview,home,Clientview,Emetteurview,CategorieEmissionServiceView,EmissionView,ServiceView,factureView
)

urlpatterns = [

    # Home Page
    path("", home.index, name="index"),
    # User Authentication
    path("user/register/",admin_required(register_view), name="user_register"),
    path("user/login/", login_view, name="user_login"),
    path("user/logout/", logout_view, name="user_logout"),
    path("user/list/",user_list_view, name="user_list"),
    # Profile Management
    path("user/profile/update/", profile_update_view, name="user_update_profile"),
    # User profile View
    path("user/profile/view/",user_view, name="user_view"),
    # User Activation (Admin)
    path("user/activate/<int:user_id>/",admin_required(user_activation_view), name="user_activation"),
    # Password Change (Logged-in Users)
    path("user/password/change/", password_change_view, name="user_password_change"),



    # Station Radio Departement URLs
    path("station_radio_departement/", admin_required(StationRadioDepartementview.index), name='station_radio_departement_index'),
    path("station_radio_departement/create/", admin_required(StationRadioDepartementview.create), name='station_radio_departement_create'),
    path("station_radio_departement/edit/<int:id>/", admin_required(StationRadioDepartementview.edit), name='station_radio_departement_edit'),
    path("station_radio_departement/delete/<int:id>/", admin_required(StationRadioDepartementview.delete), name='station_radio_departement_delete'),


    path("utilisateur_emetteur_station/", admin_required(UtilisateurEmetteurStationview.index), name='utilisateur_emetteur_index'),
    path("utilisateur_emetteur_station/create/", admin_required(UtilisateurEmetteurStationview.create), name='utilisateur_emetteur_create'),
    path("utilisateur_emetteur_station/edit/<int:id>/", admin_required(UtilisateurEmetteurStationview.edit), name='utilisateur_emetteur_edit'),
    path("utilisateur_emetteur_station/delete/<int:id>/", admin_required(UtilisateurEmetteurStationview.delete), name='utilisateur_emetteur_delete'),



    path("client/", facturier_required(Clientview.index), name='client_index'),
    path("client/create/", facturier_required(Clientview.create), name='client_create'),
    path("client/edit/<int:id>/",  admin_required(Clientview.edit), name='client_edit'),
    path("client/delete/<int:id>/",  admin_required(Clientview.delete), name='client_delete'),
    path("client/detail/<int:id>/", facturier_required(Clientview.client_detail), name='client_detail'),



    path('emetteur/', admin_required(Emetteurview.emetteur_index), name='emetteur_index'),
    path('emetteur/create/', admin_required(Emetteurview.emetteur_create), name='emetteur_create'),
    path('emetteur/edit/<int:id>/', admin_required(Emetteurview.emetteur_edit), name='emetteur_edit'),
    path('emetteur/delete/<int:id>/', admin_required(Emetteurview.emetteur_delete), name='emetteur_delete'),
    path('emetteur/detail/<int:id>/', admin_required(Emetteurview.emetteur_detail), name='emetteur_detail'),



    # Categorie Emission Service URLs
    path("categorie_emission_service/", admin_required(CategorieEmissionServiceView.index), name='categorie_emission_service_index'),
    path("categorie_emission_service/create/", admin_required(CategorieEmissionServiceView.create), name='categorie_emission_service_create'),
    path("categorie_emission_service/edit/<int:id>/", admin_required(CategorieEmissionServiceView.edit), name='categorie_emission_service_edit'),
    path("categorie_emission_service/delete/<int:id>/", admin_required(CategorieEmissionServiceView.delete), name='categorie_emission_service_delete'),

    # Emission URLs
    path("emission/", admin_required(EmissionView.emission_index), name='emission_index'),
    path("emission/create/", admin_required(EmissionView.emission_create), name='emission_create'),
    path("emission/edit/<int:id>/", admin_required(EmissionView.emission_edit), name='emission_edit'),
    path("emission/delete/<int:id>/", admin_required(EmissionView.emission_delete), name='emission_delete'),



    # Service URLs
    path("service/", admin_required(ServiceView.service_index), name='service_index'),
    path("service/create/", admin_required(ServiceView.service_create), name='service_create'),
    path("service/edit/<int:id>/", admin_required(ServiceView.service_edit), name='service_edit'),
    path("service/delete/<int:id>/", admin_required(ServiceView.service_delete), name='service_delete'),



    # Facture URLs
    path("facture/creer/", facturier_required(factureView.creer_facture), name="creer_facture"),
    path("facture/list/", facturier_required(factureView.facture_list), name="facture_list"),
    path("facture/edit/<int:id>/", admin_required(factureView.facture_edit), name="facture_edit"),
    path("facture/detail/<int:id>/", facturier_required(factureView.facture_detail), name="facture_detail"),
    path('facture/<int:id>/print/', facturier_required(factureView.facture_print), name='facture_print'),


    path("access_denied/",home.perm_is_admin, name="access_denied"),
]