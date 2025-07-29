"""Top-level package for NetBox netauto Plugin."""

__author__ = """Matej Lanca"""
__email__ = "lancamatej@gmail.com"
__version__ = "1.0.6"
__description__ = "NetBox plugin for integration with the netauto ecosystem."


from netbox.plugins import PluginConfig


class netautoConfig(PluginConfig):
    name = "netbox_netauto_plugin"
    author = __author__
    verbose_name = "Netauto"
    description = __description__
    version = __version__
    base_url = "netbox_netauto_plugin"
    min_version = "4.1"
    default_settings = {
        "ritm_choices_source": "static",
        "gitlab_repository_url": "https://gitlab.alefnula.com/customers/csob/netauto/ci-demo/",
        "default_pillar_color": "0000ff",
        "snow": {
            "url": "",
            "user": "",
            "password": ""
        }
    }


config = netautoConfig
