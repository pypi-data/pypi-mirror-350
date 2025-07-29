from django.core.exceptions import ValidationError
import ipaddress
import re

def validate_name(value):
    pattern = r'^[A-Za-z][A-Za-z0-9_.-]*$'
    if not re.match(pattern, value):
        raise ValidationError(f'{value} is not a valid name. It must start with a letter and contain only letters, numbers, underscores, dots, or hyphens.')


def validate_cidr(value):
    try:
        ipaddress.ip_network(value, strict=False)
    except ValueError:
        raise ValidationError(f'{value} is not a valid CIDR format')

def validate_cidr_list(value):
    for cidr in value.split(','):
        validate_cidr(cidr.strip())

def validate_ip_port(value):
    try:
        ip, port = value.split(':')
        ipaddress.ip_address(ip)
        port = int(port)
        if port < 1 or port > 65535:
            raise ValueError
    except ValueError:
        raise ValidationError(f'{value} is not a valid IP:PORT format')
    
def validate_ip_port_list(value):
    for ip_port in value.split(','):
        validate_ip_port(ip_port.strip())


def validate_at_least_one_set(primary_set: set, secondary_set: set):
    if not any(primary_set) and not all(secondary_set):
        raise ValidationError(f'At least one of {primary_set} or {secondary_set} must be set')
    
class AtLeastOneSetValidator:
    def __init__(self, primary_set: set, secondary_set: set):
        self.primary_set = primary_set
        self.secondary_set = secondary_set

    def __call__(self, instance):
        primary_set_valid = any(getattr(instance, attr).exists() if hasattr(getattr(instance, attr), 'exists') else getattr(instance, attr) for attr in self.primary_set)
        secondary_set_valid = all(getattr(instance, attr).exists() if hasattr(getattr(instance, attr), 'exists') else getattr(instance, attr) for attr in self.secondary_set)
        if not primary_set_valid and not secondary_set_valid:
            raise ValidationError(f'At least one of {self.primary_set} or {self.secondary_set} must be set')