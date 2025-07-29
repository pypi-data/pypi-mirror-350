from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from . import models, views


urlpatterns = (
    # Profiles
    path("profiles/", views.ProfileListView.as_view(), name="profile_list"),
    path("profiles/add/", views.ProfileEditView.as_view(), name="profile_add"),
    path("profiles/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("profiles/<int:pk>/edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    path("profiles/<int:pk>/delete/", views.ProfileDeleteView.as_view(), name="profile_delete"),
    path(
        "profiles/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="profile_changelog",
        kwargs={"model": models.Profile},
    ),
    path("profiles/import/", views.ProfileBulkImportView.as_view(), name="profile_import"),
    path("profiles/edit/", views.ProfileBulkEditView.as_view(), name="profile_bulk_edit"),
    path("profiles/delete/", views.ProfileBulkDeleteView.as_view(), name="profile_bulk_delete"),
    
    # Flex Applications
    path("flex-applications/", views.FlexApplicationListView.as_view(), name="flexapplication_list"),
    path("flex-applications/add/", views.FlexApplicationEditView.as_view(), name="flexapplication_add"),
    path("flex-applications/<int:pk>/", views.FlexApplicationView.as_view(), name="flexapplication"),
    path("flex-applications/<int:pk>/edit/", views.FlexApplicationEditView.as_view(), name="flexapplication_edit"),
    path("flex-applications/<int:pk>/delete/", views.FlexApplicationDeleteView.as_view(), name="flexapplication_delete"),
    path(
        "flex-applications/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(base_template="application.html"),
        name="flexapplication_changelog",
        kwargs={"model": models.FlexApplication},
    ),

    # L4 Applications
    path("l4-applications/", views.L4ApplicationListView.as_view(), name="l4application_list"),
    path("l4-applications/add/", views.L4ApplicationEditView.as_view(), name="l4application_add"),
    path("l4-applications/<int:pk>/", views.L4ApplicationView.as_view(), name="l4application"),
    path("l4-applications/<int:pk>/edit/", views.L4ApplicationEditView.as_view(), name="l4application_edit"),
    path("l4-applications/<int:pk>/delete/", views.L4ApplicationDeleteView.as_view(), name="l4application_delete"),
    path(
        "l4-applications/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(base_template="application.html"),
        name="l4application_changelog",
        kwargs={"model": models.L4Application},
    ),

    # mTLS Applications

    path("mtls-applications/", views.mTLSApplicationListView.as_view(), name="mtlsapplication_list"),
    path("mtls-applications/add/", views.mTLSApplicationEditView.as_view(), name="mtlsapplication_add"),
    path("mtls-applications/<int:pk>/", views.mTLSApplicationView.as_view(), name="mtlsapplication"),
    path("mtls-applications/<int:pk>/edit/", views.mTLSApplicationEditView.as_view(), name="mtlsapplication_edit"),
    path("mtls-applications/<int:pk>/delete/", views.mTLSApplicationDeleteView.as_view(), name="mtlsapplication_delete"),
    path(
        "mtls-applications/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(base_template="application.html"),
        name="mtlsapplication_changelog",
        kwargs={"model": models.mTLSApplication},
    ),
)
