from django.db.models import Count

from netbox.views import generic
from . import filtersets, forms, models, tables

# Profiles

class ProfileView(generic.ObjectView):
    queryset = models.Profile.objects.all()
    template_name = "profile.html"

class ProfileListView(generic.ObjectListView):
    queryset = models.Profile.objects.all()
    table = tables.ProfileTable
    filterset = filtersets.ProfileFilterSet
    filterset_form = forms.ProfileFilterForm

class ProfileEditView(generic.ObjectEditView):
    queryset = models.Profile.objects.all()
    form = forms.ProfileForm

class ProfileDeleteView(generic.ObjectDeleteView):
    queryset = models.Profile.objects.all()

class ProfileBulkImportView(generic.BulkImportView):
    queryset = models.Profile.objects.all()
    model_form = forms.ProfileImportForm
    table = tables.ProfileTable

class ProfileBulkEditView(generic.BulkEditView):
    queryset = models.Profile.objects.all()
    filterset = filtersets.ProfileFilterSet
    table = tables.ProfileTable
    form = forms.ProfileBulkEditForm

class ProfileBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Profile.objects.all()
    table = tables.ProfileTable

# Flex Applications

class FlexApplicationView(generic.ObjectView):
    queryset = models.FlexApplication.objects.all()
    template_name = "application.html"


class FlexApplicationListView(generic.ObjectListView):
    queryset = models.FlexApplication.objects.all()
    table = tables.FlexApplicationTable
    filterset = filtersets.FlexApplicationFilterSet
    filterset_form = forms.FlexApplicationFilterForm


class FlexApplicationEditView(generic.ObjectEditView):
    queryset = models.FlexApplication.objects.all()
    form = forms.FlexApplicationForm
    template_name = "application_edit.html"


class FlexApplicationDeleteView(generic.ObjectDeleteView):
    queryset = models.FlexApplication.objects.all()


# L4 Applications

class L4ApplicationView(generic.ObjectView):
    queryset = models.L4Application.objects.all()
    template_name = "application.html"

class L4ApplicationListView(generic.ObjectListView):
    queryset = models.L4Application.objects.all()
    table = tables.L4ApplicationTable
    filterset = filtersets.L4ApplicationFilterSet
    filterset_form = forms.L4ApplicationFilterForm

class L4ApplicationEditView(generic.ObjectEditView):
    queryset = models.L4Application.objects.all()
    form = forms.L4ApplicationForm
    template_name = "application_edit.html"

class L4ApplicationDeleteView(generic.ObjectDeleteView):
    queryset = models.L4Application.objects.all()


# mTLS Applications

class mTLSApplicationView(generic.ObjectView):
    queryset = models.mTLSApplication.objects.all()
    template_name = "application.html"

class mTLSApplicationListView(generic.ObjectListView):
    queryset = models.mTLSApplication.objects.all()
    table = tables.mTLSApplicationTable
    filterset = filtersets.mTLSApplicationFilterSet
    filterset_form = forms.mTLSApplicationFilterForm

class mTLSApplicationEditView(generic.ObjectEditView):
    queryset = models.mTLSApplication.objects.all()
    form = forms.mTLSApplicationForm
    template_name = "application_edit.html"

class mTLSApplicationDeleteView(generic.ObjectDeleteView):
    queryset = models.mTLSApplication.objects.all()
