from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox.api.fields import ChoiceField
from ipam.api.serializers import IPAddressSerializer, VLANSerializer
from tenancy.api.serializers import TenantSerializer
from dcim.api.serializers import VirtualChassisSerializer
from .. import models
from .. import choices


class MyVirtualChassisSerializer(VirtualChassisSerializer):
    class Meta(VirtualChassisSerializer.Meta):
        brief_fields = VirtualChassisSerializer.Meta.brief_fields + ('custom_fields',)

class MyVLANSerializer(VLANSerializer):
    class Meta(VLANSerializer.Meta):
        brief_fields = VLANSerializer.Meta.brief_fields + ('custom_fields',)


class ProfileSerializer(NetBoxModelSerializer):
    type = ChoiceField(
        choices=choices.ProfileTypeChoices,
        required=False
    )
    cluster = VirtualChassisSerializer(
        nested=True, 
        read_only=True
    )

    class Meta:
        model = models.Profile
        fields = (
            "id",
            "name",
            "display",
            "type",
            "cluster",
            "comments",
            "last_updated"
        )
        brief_fields = (
            "id",
            "name",
            "display",
            "type"
        )
        

class ApplicationSerializer(NetBoxModelSerializer):
    tenant = TenantSerializer(
        nested=True, 
        read_only=True
    )
    cluster = MyVirtualChassisSerializer(
        nested=True, 
        read_only=True
    )
    virtual_ip_address = IPAddressSerializer(
        nested=True, 
        read_only=True
    )
    persistence_profile = ProfileSerializer(
        nested=True, 
        read_only=True
    )
    status = ChoiceField(
        choices=choices.ApplicationStatusChoices, 
        required=False
    )
    name = serializers.CharField(
        required=False
    )

    # class Meta:
        # fields = (
        #     "id",
        #     "display",
        #     "status",
        #     "ritm",
        #     "name",
        #     "description",
        #     "tenant",
        #     "cluster",
        #     "virtual_ip_address",
        #     "virtual_ip_address_string",
        #     "virtual_port",
        #     "member_ip_addresses_string",
        #     "persistence_profile",
        #     "last_updated"
        # )

class HTTPApplicationSerializer(ApplicationSerializer):
    tcp_wan = ProfileSerializer(
        nested=True, 
        read_only=True
    )
    tcp_lan = ProfileSerializer(
        nested=True, 
        read_only=True
    )
    http = ProfileSerializer(
        nested=True, 
        read_only=True
    )
    client_ssl_profile = ProfileSerializer(
        nested=True, 
        read_only=True
    )
    server_ssl_profile = ProfileSerializer(
        nested=True, 
        read_only=True
    )
    oneconnect_profile = ProfileSerializer(
        nested=True, 
        read_only=True
    )
    health_monitor_profile = ProfileSerializer(
        nested=True, 
        read_only=True
    )

    # class Meta:
        # fields = ApplicationSerializer.Meta.fields + (
        #     "tcp_wan",
        #     "tcp_lan",
        #     "http",
        #     "client_ssl_profile",
        #     "client_ssl_certificate",
        #     "client_ssl_auth_mode",
        #     "client_ssl_cert_authority",
        #     "server_ssl_profile",
        #     "oneconnect_profile",
        #     "health_monitor_profile",
        #     "send_string",
        #     "receive_string",
        #     "interval",
        #     "timeout"
        # )

class FlexApplicationSerializer(HTTPApplicationSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_netauto_plugin-api:flexapplication-detail'
    )

    class Meta:
        model = models.FlexApplication
        fields = "__all__"
        # fields = HTTPApplicationSerializer.Meta.fields + (
        #     "url",
        #     "access_profile",
        # )
        brief_fields = (
            "id",
            "url",
            "display",
        )
        
class L4ApplicationSerializer(ApplicationSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_netauto_plugin-api:l4application-detail'
    )
    fastl4 = ProfileSerializer(
        nested=True, 
        read_only=True
    )
    vlan = MyVLANSerializer(
        nested=True, 
        read_only=True
    )

    class Meta:
        model = models.L4Application
        fields = "__all__"
        # fields = ApplicationSerializer.Meta.fields + (
        #     "url",
        #     "fastl4",
        #     "vlan"
        # )

class mTLSApplicationSerializer(HTTPApplicationSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_netauto_plugin-api:mtlsapplication-detail'
    )
    vlan = MyVLANSerializer(
        nested=True, 
        read_only=True
    )

    class Meta:
        model = models.mTLSApplication
        fields = "__all__"
        # fields = HTTPApplicationSerializer.Meta.fields + (
        #     "url",
        #     "redirect_from_http",
        #     "vlan"
        # )