# NetBox netauto Plugin

NetBox plugin for integration with the netauto ecosystem.


* Free software: Apache-2.0
* Documentation: https://lancamat1.github.io/netbox-netauto-plugin/


## Features

The features the plugin provides should be listed here.

## Compatibility

| NetBox Version | Plugin Version |
|----------------|----------------|
|     >=4.0      |     >=1.0.0    |

## Installing

For adding to a NetBox Docker setup see
[the general instructions for using netbox-docker with plugins](https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins).

While this is still in development and not yet on pypi you can install with pip:

```bash
pip install git+https://github.com/lancamat1/netbox-netauto-plugin
```

or by adding to your `local_requirements.txt` or `plugin_requirements.txt` (netbox-docker):

```bash
git+https://github.com/lancamat1/netbox-netauto-plugin
```

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`,
 or if you use netbox-docker, your `/configuration/plugins.py` file :

```python
PLUGINS = [
    'netbox_netauto_plugin'
]

PLUGINS_CONFIG = {
    "netbox_netauto_plugin": {},
}
```

## Configuration

The following settings are available to configure the plugin:
- 'ritm_choices_source'
    - __type__: str
    - __description__: The source of the choices for the RITM field.
    - __default__: 'static'
    - __choices__: ['static', 'api']
- 'snow_api_url'
    - __type__: str
    - __description__: The URL of the ServiceNow API.
    - __default__: ''
- 'snow_api_token'
    - __type__: str
    - __description__: The token to authenticate with the ServiceNow API.
    - __default__: ''
- 'gitlab_repository_url'
    - __type__: str
    - __description__: The URL of the GitLab repository.
    - __default__: 'https://gitlab.alefnula.com/customers/csob/netauto/ci-demo/'
- 'default_pillar_color'
    - __type__: str
    - __description__: Tag color for pillar filter.
    - __default__: '0000ff'