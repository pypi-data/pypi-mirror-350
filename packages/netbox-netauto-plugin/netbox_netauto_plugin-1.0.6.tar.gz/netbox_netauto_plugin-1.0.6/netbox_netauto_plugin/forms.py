from django import forms
from ipam.models import IPAddress, VLAN
from tenancy.models import Tenant
from dcim.models import VirtualChassis
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelImportForm, NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, CommentField, CSVModelMultipleChoiceField
from utilities.forms.rendering import FieldSet, TabbedGroups, InlineFields, ObjectAttribute
from utilities.forms import add_blank_choice
from django.conf import settings
from django.core.exceptions import ValidationError

from . import models
from . import choices
from .utils import get_initial_ip, get_ritm_choices

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_netauto_plugin', dict())


class ProfileForm(NetBoxModelForm):
    comments = CommentField()
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        query_params={'color': plugin_settings.get('default_pillar_color')},
        label='Pillar',
        required=True,
    )
    fieldsets = (
        FieldSet(
            "name",
            "type",
            "cluster",
            "tags",
            name="Profile"
        ),
    )

    class Meta:
        model = models.Profile
        fields = "__all__"
    

class ProfileFilterForm(NetBoxModelFilterSetForm):
    model = models.Profile

class ProfileImportForm(NetBoxModelImportForm):
    tags = CSVModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=True,
        to_field_name='slug',
        help_text='Tag slugs separated by commas, encased with double quotes (e.g. "tag1,tag2,tag3")'
    )
    class Meta:
        model = models.Profile
        fields = ("name", "type", "cluster", "comments", "tags")

class ProfileBulkEditForm(NetBoxModelBulkEditForm):
    model = models.Profile
    name = forms.CharField(
        required=False,
        label='Name'
    )
    type = forms.ChoiceField(
        choices=choices.ProfileTypeChoices,
        required=False,
        label='Type'
    )
    cluster = DynamicModelChoiceField(
        queryset=VirtualChassis.objects.all(),
        label='Cluster',
        required=False,
    )
    comments = CommentField(
        required=False,
        label='Comments'
    )
    
    fieldsets = (
        FieldSet('name', 'type', 'cluster', 'tags', name='Profile'),
        FieldSet('comments', name='Comments'),
    )
    nullable_fields = ['comments']


class ApplicationForm(NetBoxModelForm):
    ritm = forms.ChoiceField(
        label="RITM",
        required=False,
        choices=(),
    )
    name = forms.CharField(
        label="Name",
        required=True,
    )
    description = forms.CharField(
        label="Description",
        required=False,
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        selector=True,
    )
    virtual_ip_address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        query_params={'tenant_id': '$tenant'},
        required=False,
        selector=True,
        label="Virtual IP Address",
        help_text="Select the destination IP address."
    )
    virtual_ip_address_string = forms.CharField(
        label="Virtual IP Address",
        required=False,
        help_text="Enter the destination IP address with a mask. Initial value is the first available IP address in the VIP prefix.",
    )
    member_ip_addresses_string = forms.CharField(
        label="Pool member IP Addresses",
        help_text="Enter the member IP addresses with ports separated by commas. Example: '1.1.1.1:80, 2.2.2.2:8080'",
    )
    send_string = forms.CharField(
        label="Send String",
        required=False,
    )
    receive_string = forms.CharField(
        label="Receive String",
        required=False,
    )
    persistence_profile = DynamicModelChoiceField(
        queryset=models.Profile.objects.all(),
        query_params={
            'type': choices.ProfileTypeChoices.PERSISTENCE,
            'cluster': '$cluster',
            'tags': '$tags'
        },
        label="Persistence Profile",
        required=False,
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        query_params={'color': plugin_settings.get('default_pillar_color')},
        label='Pillar',
    )

    class Meta:
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_ip_info = get_initial_ip() if self.instance._state.adding else {}
        self.vrf = initial_ip_info.get('vrf')
        if not self.instance._state.adding:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['ritm'].widget.attrs['readonly'] = True
        else:
            self.initial['virtual_ip_address_string'] = initial_ip_info.get('ip')
            self.fields['ritm'].choices = add_blank_choice(get_ritm_choices())

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', [])
        if len(tags) != 1:
            raise ValidationError("Exactly one pillar must be selected.")

        if tags and self.instance.cluster:
            for tag in tags:
                if not self.instance.cluster.tags.filter(name=tag.name).exists():
                    self.add_error('tags', f"Cluster {self.instance.cluster} does not have tag {tag.name}")
        return tags

    
    # on form submission set status to New -> leads to triggering pipeline
    # where as setting status to other values over API does not trigger pipeline
    def save(self, *args, **kwargs):
        if not self.instance._state.adding:
            self.instance.status = choices.ApplicationStatusChoices.UPDATE

        self.instance.vrf = self.vrf
        return super().save(*args, **kwargs)


class HTTPApplicationForm(ApplicationForm):

    tcp_wan = DynamicModelChoiceField(
        queryset=models.Profile.objects.all(),
        query_params={
            'type': choices.ProfileTypeChoices.TCP,
            'cluster': '$cluster',
            'tags': '$tags'
        },
        label="TCP WAN Profile",
    )
    tcp_lan = DynamicModelChoiceField(
        queryset=models.Profile.objects.all(),
        query_params={
            'type': choices.ProfileTypeChoices.TCP,
            'cluster': '$cluster',
            'tags': '$tags'
        },
        label="TCP LAN Profile",
    )
    http = DynamicModelChoiceField(
        queryset=models.Profile.objects.all(),
        query_params={
            'type': choices.ProfileTypeChoices.HTTP,
            'cluster': '$cluster',
            'tags': '$tags'
        },
        label="HTTP Profile",
    )
    client_ssl_profile = DynamicModelChoiceField(
        queryset=models.Profile.objects.all(),
        query_params={
            'type': choices.ProfileTypeChoices.CLIENT_SSL,
            'cluster': '$cluster',
            'tags': '$tags'
        },
        label="Client SSL Profile",
        required=False,
    )
    server_ssl_profile = DynamicModelChoiceField(
        queryset=models.Profile.objects.all(),
        query_params={
            'type': choices.ProfileTypeChoices.SERVER_SSL,
            'cluster': '$cluster',
            'tags': '$tags'
        },
        label="Server SSL Profile",
        required=False,
    )
    oneconnect_profile = DynamicModelChoiceField(
        queryset=models.Profile.objects.all(),
        query_params={
            'type': choices.ProfileTypeChoices.ONECONNECT,
            'cluster': '$cluster',
            'tags': '$tags'
        },
        label="OneConnect Profile",
    )
    health_monitor_profile = DynamicModelChoiceField(
        queryset=models.Profile.objects.all(),
        query_params={
            'type': choices.ProfileTypeChoices.HEALTH_MONITOR,
            'cluster': '$cluster',
            'tags': '$tags'
        },
        label="Health Monitor Profile",
        required=False,
    )
    

class FlexApplicationForm(HTTPApplicationForm):
    cluster = DynamicModelChoiceField(
        queryset=VirtualChassis.objects.all(),
        query_params={'tag': 'f5-flex'},
        selector=True,
        help_text="The cluster is pre-filtered with the 'f5-flex' tag."
    )

    client_ssl_profile = DynamicModelChoiceField(
        queryset=models.Profile.objects.all(),
        query_params={
            'type': choices.ProfileTypeChoices.CLIENT_SSL,
            'cluster': '$cluster',
            'tags': '$tags'
        },
        label="Client SSL Profile",
    )

    access_profile = forms.CharField(
        label="Access profile",
        required=False,
        help_text="Enter the access profile name exactly as configured on the F5 device.",
    )

    fieldsets = (
        FieldSet(
            "name",
            "tenant", 
            "tags",
            "cluster",
            TabbedGroups(
                FieldSet("virtual_ip_address", name="IP Address Object"),
                FieldSet("virtual_ip_address_string", name="CIDR String"),
            ),
            "virtual_port", 
            "member_ip_addresses_string",
            "description",
            name="Application Details"
        ),
        FieldSet(
            "tcp_wan", 
            "tcp_lan",
            "persistence_profile", 
            "http", 
            "client_ssl_profile",
            "server_ssl_profile", 
            "oneconnect_profile",
            "access_profile",
            name="Profiles"
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("health_monitor_profile", name="Existing"),
                FieldSet("send_string", "receive_string", "interval", "timeout", name="Custom"),
            ),
            name="Health Monitor"
        ),
        FieldSet(
            "irule",
            name="iRule",
        )
    )

    class Meta(HTTPApplicationForm.Meta):
        model = models.FlexApplication

class FlexApplicationFilterForm(NetBoxModelFilterSetForm):
    model = models.FlexApplication


class L4ApplicationForm(ApplicationForm):
    cluster = DynamicModelChoiceField(
        queryset=VirtualChassis.objects.all(),
        query_params={'tag': 'f5-l4'},
        selector=True,
        help_text="The cluster is pre-filtered with the 'f5-l4' tag."
    )

    fastl4 = DynamicModelChoiceField(
        queryset=models.Profile.objects.all(),
        query_params={
            'type': choices.ProfileTypeChoices.FASTL4,
            'cluster': '$cluster',
            'tags': '$tags'
        },
        label="FastL4 Profile",
    )

    vlan = DynamicModelChoiceField(
        queryset=VLAN.objects.all(),
        required=True,
        selector=True,
        label="Allowed VLAN",
        help_text="Select the allowed VLAN.",
        # context={"label": ""}
    )

    fieldsets = (
        FieldSet(
            "name",
            "tenant", 
            "tags",
            "cluster",
            "vlan",
            TabbedGroups(
                FieldSet("virtual_ip_address", name="IP Address Object"),
                FieldSet("virtual_ip_address_string", name="CIDR String"),
            ),
            "virtual_port", 
            "member_ip_addresses_string",
            "description",
            name="Application Details"
        ),
        FieldSet(
            "fastl4",
            "persistence_profile", 
            name="Profiles"
        ),
    )

    class Meta(ApplicationForm.Meta):
        model = models.L4Application

class L4ApplicationFilterForm(NetBoxModelFilterSetForm):
    model = models.L4Application


class mTLSApplicationForm(HTTPApplicationForm):
    cluster = DynamicModelChoiceField(
        queryset=VirtualChassis.objects.all(),
        query_params={'tag': 'f5-mtls'},
        selector=True,
        help_text="The cluster is pre-filtered with the 'f5-mtls' tag."
    )

    vlan = DynamicModelChoiceField(
        queryset=VLAN.objects.all(),
        required=True,
        selector=True,
        label="Allowed VLAN",
        help_text="Select the allowed VLAN."
    )

    fieldsets = (
        FieldSet(
            "name",
            "tenant", 
            "tags",
            "cluster",
            "vlan",
            TabbedGroups(
                FieldSet("virtual_ip_address", name="IP Address Object"),
                FieldSet("virtual_ip_address_string", name="CIDR String"),
            ),
            "virtual_port", 
            "member_ip_addresses_string",
            "redirect_from_http",
            "description",
            name="Application Details"
        ),
        FieldSet(
            "tcp_wan", 
            "tcp_lan",
            "persistence_profile", 
            "http", 
            "server_ssl_profile", 
            "oneconnect_profile",
            name="Profiles"
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("client_ssl_profile", name="Existing"),
                FieldSet("client_ssl_certificate", "client_ssl_auth_mode", "client_ssl_cert_authority", "client_ssl_server_name", name="Custom")
            ),
            name="Client SSL Profile"
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("health_monitor_profile", name="Existing"),
                FieldSet("send_string", "receive_string", "interval", "timeout", name="Custom"),
            ),
            name="Health Monitor"
        ),
        FieldSet(
            "irule",
            name="iRule",
        )
    )

    class Meta(HTTPApplicationForm.Meta):
        model = models.mTLSApplication

class mTLSApplicationFilterForm(NetBoxModelFilterSetForm):
    model = models.mTLSApplication

    