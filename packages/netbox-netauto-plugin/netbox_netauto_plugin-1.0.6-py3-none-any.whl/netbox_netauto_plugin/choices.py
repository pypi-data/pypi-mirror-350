from utilities.choices import ChoiceSet

class ClientSSLAuthModeChoices(ChoiceSet):
    REQUIRED = 'required'
    REQUEST = 'request'
    IGNORE = 'ignore'

    CHOICES = (
        (REQUIRED, 'Required', 'green'),
        (REQUEST, 'Request', 'orange'),
        (IGNORE, 'Ignore', 'red'),
    )

class ClientSSLCertAuthorityChoices(ChoiceSet):
    BUNDLE = 'bundle'

    CHOICES = (
        (BUNDLE, 'TCZ_bundle', 'green'),
    )

class ProfileTypeChoices(ChoiceSet):
    TCP = 'tcp'
    FASTL4 = 'fastl4'
    HTTP = 'http'
    CLIENT_SSL = 'client_ssl'
    SERVER_SSL = 'server_ssl'
    ONECONNECT = 'oneconnect'
    PERSISTENCE = 'persistence'
    HEALTH_MONITOR = 'health_monitor'

    CHOICES = [
        (TCP, 'TCP', 'blue'),
        (FASTL4, 'FastL4', 'brown'),
        (HTTP, 'HTTP', 'green'),
        (CLIENT_SSL, 'Client SSL', 'purple'),
        (SERVER_SSL, 'Server SSL', 'orange'),
        (ONECONNECT, 'OneConnect', 'yellow'),
        (PERSISTENCE, 'Persistence', 'red'),
        (HEALTH_MONITOR, 'Health Monitor', 'cyan'),
    ]

    
class ApplicationStatusChoices(ChoiceSet):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    PROVISIONING = 'provisioning'
    BUILDING = 'building'
    MERGE = 'merge'
    SUCCESS = 'success'
    FAILED = 'failed'

    CHOICES = (
        (CREATE, 'Creating', 'cyan'),
        (UPDATE, 'Updating', 'blue'),
        (DELETE, 'Deleting', 'red'),
        (PROVISIONING, 'Provisioning', 'orange'),
        (BUILDING, 'Building configuration', 'purple'),
        (MERGE, 'Merge pending', 'yellow'),
        (SUCCESS, 'Success', 'green'),
        (FAILED, 'Failed', 'red'),
    )