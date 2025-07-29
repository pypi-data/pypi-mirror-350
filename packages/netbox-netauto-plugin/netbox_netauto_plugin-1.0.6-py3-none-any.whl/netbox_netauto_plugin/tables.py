import django_tables2 as tables
from netbox.tables import NetBoxTable, ChoiceFieldColumn, TagColumn

from . import models

class ProfileTable(NetBoxTable):
    name = tables.Column(linkify=True)
    type = ChoiceFieldColumn()
    cluster = tables.Column(linkify=True)
    tags = TagColumn(url_name='plugins:netbox_netauto_plugin:profile_list')

    class Meta(NetBoxTable.Meta):
        model = models.Profile
        fields = (
            "pk",
            "id",
            "name",
            "type",
            "cluster",
            "comments",
            "tags",
            "actions"
        )
        default_columns = (
            "name",
            "type",
            "cluster",
            "tags"
        )


class ApplicationTable(NetBoxTable):
    name = tables.Column(linkify=True)
    virtual_ip_address = tables.Column(linkify=True)
    cluster = tables.Column(linkify=True)
    tenant = tables.Column(linkify=True)
    status = ChoiceFieldColumn()
    tcp_wan = ChoiceFieldColumn()
    tcp_lan = ChoiceFieldColumn()
    persistence_profile = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        fields = (
            "pk",
            "id",
            "name",
            "description",
            "status",
            "cluster",
            "tenant",
            "virtual_ip_address",
            "virtual_port",
            "member_ip_addresses_string",
            "tcp_wan",
            "tcp_lan",
            "persistence_profile",
            "actions",
            "tags"
        )
        default_columns = (
            "name",
            "status",
            "virtual_ip_address",
            "cluster",
            "dst_port"
        )


class HTTPApplicationTable(ApplicationTable):
    http = ChoiceFieldColumn()
    client_ssl_profile = ChoiceFieldColumn()
    server_ssl_profile = ChoiceFieldColumn()
    oneconnect_profile = ChoiceFieldColumn()
    health_monitor_profile = ChoiceFieldColumn()

    class Meta(ApplicationTable.Meta):
        fields = ApplicationTable.Meta.fields + (
            "tcp_wan", 
            "tcp_lan",
            "http", 
            "client_ssl_profile", 
            "server_ssl_profile", 
            "oneconnect_profile", 
            "health_monitor_profile", 
            "send_string", 
            "receive_string", 
            "interval", 
            "timeout", 
            "client_ssl_server_name",
            "client_ssl_certificate", 
            "client_ssl_auth_mode", 
            "client_ssl_cert_authority",
        )

class FlexApplicationTable(HTTPApplicationTable):
    tags = TagColumn(url_name='plugins:netbox_netauto_plugin:flexapplication_list')
    vlan = tables.Column(linkify=True)
        
    class Meta(HTTPApplicationTable.Meta):
        model = models.FlexApplication
        fields = HTTPApplicationTable.Meta.fields + (
            "vlan",
        )


class L4ApplicationTable(ApplicationTable):
    tags = TagColumn(url_name='plugins:netbox_netauto_plugin:l4application_list')
    vlan = tables.Column(linkify=True)

    class Meta(ApplicationTable.Meta):
        model = models.L4Application
        fields = ApplicationTable.Meta.fields + (
            "vlan",
        )


class mTLSApplicationTable(HTTPApplicationTable):
    tags = TagColumn(url_name='plugins:netbox_netauto_plugin:mtlsapplication_list')

    class Meta(HTTPApplicationTable.Meta):
        model = models.mTLSApplication