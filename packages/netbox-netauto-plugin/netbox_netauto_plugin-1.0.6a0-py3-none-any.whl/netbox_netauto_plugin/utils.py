from ipam.models import Prefix, Role
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_netauto_plugin', dict())

def get_all_subclasses(cls):
    subclasses = set(cls.__subclasses__())
    for subclass in subclasses.copy():
        subclasses.update(get_all_subclasses(subclass))
    return subclasses

def get_initial_ip():
    try:
        vip_role = Role.objects.get(slug='vip')
        for prefix in Prefix.objects.filter(role=vip_role):
            if prefix.get_first_available_ip() is not None:
                return {
                    'ip': prefix.get_first_available_ip(),
                    'vrf': prefix.vrf
                }
            
        else:
            raise ValueError("No available IP addresses found in the VIP prefixes")
    except Role.DoesNotExist:
        pass

def get_tasks(url, auth):
    import requests

    try:
        response = requests.get(f"{url}/get_impl_tasks", auth=auth, timeout=5)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise ValueError("The request to the ServiceNow API timed out after 5 seconds")
    except requests.exceptions.HTTPError as e:
        raise ValueError(f"Failed to get tasks from the ServiceNow API: {e}")
    
    return response.json().get('result')

def get_ritm_choices():
    data = dict()
    if plugin_settings.get('ritm_choices_source') == 'api':
        snow_api_url = plugin_settings.get('snow').get('url')
        snow_api_auth = (plugin_settings.get('snow').get('user'), plugin_settings.get('snow').get('password'))
        if not snow_api_auth or not snow_api_url:
            raise ImproperlyConfigured("url, user and password must be set in the plugin settings for the 'api' ritm_choices_source")

        data['result'] = get_tasks(snow_api_url, snow_api_auth)
    elif plugin_settings.get('ritm_choices_source') == 'static':
        data['result'] = [
            {
                "sys_id": "c40fddd3972579d0c8c7b18fe153afbf",
                "short_description": "Loadbalancing Service Request (NEW) - cloudbhub.cz.intapp.eu"
            },
            {
                "sys_id": "bafbbe0cdbb2f1142c554d7605961945",
                "short_description": "Loadbalancing Service Request (NEW) - fnbpm2.cz.dev.intapp.eu"
            },
            {
                "sys_id": "236c8ace87b3b590cd76b91c8bbb352b",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "c88c8a4287f3b590cd76b91c8bbb359f",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "85495cf3c33fb590b1f35c94e40131d7",
                "short_description": "Delete Load Balancing Service"
            },
            {
                "sys_id": "2e7bd8f7c37fb590b1f35c94e401318f",
                "short_description": "Delete Load Balancing Service"
            },
            {
                "sys_id": "6cf3889c87188ad0cd76b91c8bbb35b1",
                "short_description": "Delete Load Balancing Servicecloudbhub.cz.int.intapp.eu"
            },
            {
                "sys_id": "24845ef1475c8e14cef78054f26d4343",
                "short_description": "Loadbalancing Service Request (NEW) - earnixahu.csobpoj.cz"
            },
            {
                "sys_id": "5f3a2ec11ba84e5063e71022b24bcb68",
                "short_description": "Delete Load Balancing Service"
            },
            {
                "sys_id": "7b0be2091ba84e5063e71022b24bcbdd",
                "short_description": "Delete Load Balancing Service"
            },
            {
                "sys_id": "8222444a97918a90c277b06de053af19",
                "short_description": "Loadbalancing Service Request (MODIFY) - fngsapp.cz.intapp.eu"
            },
            {
                "sys_id": "2035449a97dd82905677f89fe153af96",
                "short_description": "Loadbalancing Service Request (NEW) - scaler-int"
            },
            {
                "sys_id": "34d2438bc3ee4e187fd8d3dc7a0131bf",
                "short_description": "Loadbalancing Service Request (MODIFY) - "
            },
            {
                "sys_id": "638b26a1c38b4a5041ed3dd6050131a1",
                "short_description": "Loadbalancing Service Request (MODIFY) - "
            },
            {
                "sys_id": "5957b335c3cb46107fd8d3dc7a0131c7",
                "short_description": "Loadbalancing Service Request (MODIFY) - genesysmobile.csob.cz"
            },
            {
                "sys_id": "12ecdf52c3438210f12fd4677a0131f4",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "a06bd3cbc3cf4a1041ed3dd605013153",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "5250dc53c3434a507fd8d3dc7a01310a",
                "short_description": "CZ_CREATE/MODIFY/CANCEL DNS APPLICATION ALIAS (CNAME)"
            },
            {
                "sys_id": "979739efc3c78250f12fd4677a01315b",
                "short_description": "The Implementation task for CZ DC part of Firewall rule"
            },
            {
                "sys_id": "6a9af9ab47cb8650cef78054f26d435c",
                "short_description": "The Implementation task for CZ DC part of Firewall rule"
            },
            {
                "sys_id": "f332ca7383834a50620390c5eeaad30d",
                "short_description": "The Implementation task for CZ DC part of Firewall rule"
            },
            {
                "sys_id": "8b62c6b383834a50620390c5eeaad391",
                "short_description": "The Implementation task for CZ DC part of Firewall rule"
            },
            {
                "sys_id": "efb2023783430a905ea79d65eeaad38c",
                "short_description": "The Implementation task for CZ DC part of Firewall rule"
            },
            {
                "sys_id": "dea386f783834a50620390c5eeaad35e",
                "short_description": "The Implementation task for CZ DC part of Firewall rule"
            },
            {
                "sys_id": "0e454af3c3c38a50ea133b1f05013140",
                "short_description": "The Implementation task for CZ DC part of Firewall rule"
            },
            {
                "sys_id": "fb793a3fc3430e508f9637da05013129",
                "short_description": "The Implementation task for CZ DC part of Firewall rule"
            },
            {
                "sys_id": "3b559281c393c210b1f35c94e4013117",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "bb559281c393c210b1f35c94e4013181",
                "short_description": "The Implementation task for CZ Perimeter part of Firewall rule"
            },
            {
                "sys_id": "c3750b4983d786105ea79d65eeaad3ab",
                "short_description": "The Implementation task for CZ AWS part of Firewall rule"
            },
            {
                "sys_id": "13750b4983d786105ea79d65eeaad3bf",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "c59847cd831b86105ea79d65eeaad3ed",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "de984bcd831b86105ea79d65eeaad391",
                "short_description": "The Implementation task for CZ AWS part of Firewall rule"
            },
            {
                "sys_id": "1a984bcd831b86105ea79d65eeaad3a3",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "a398cbcd831b86105ea79d65eeaad30b",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "24a80fcd831b86105ea79d65eeaad370",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "aca80fcd831b86105ea79d65eeaad38d",
                "short_description": "The Implementation task for CZ DC part of Firewall rule"
            },
            {
                "sys_id": "21a80301835b86105ea79d65eeaad316",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "6a9ccb45c397461041ed3dd6050131a2",
                "short_description": "The Implementation task for CEDC-CZ Tenant part of Firewall rule"
            },
            {
                "sys_id": "4c4fd781471746105338a942036d43e9",
                "short_description": "The Implementation task for CZ DC part of Firewall rule"
            },
            {
                "sys_id": "3a1c2b89c39746108f9637da05013197",
                "short_description": "Loadbalancing Service Request (NEW) - glowotp.prod.apps.cz"
            }
        ]
    return [(task['sys_id'], f"{task['sys_id']} > {task['short_description']}") for task in data['result']]