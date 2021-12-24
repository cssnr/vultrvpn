import base64
import os
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core import management
from .vultr import Vultr

logger = get_task_logger(__name__)


FAKE = {
    'allowed_bandwidth': 1000,
    'app_id': 0,
    'date_created': '2021-12-23T18:28:06-05:00',
    'default_password': 'Y]k2BLUVKNYYAMNs',
    'disk': 0,
    'features': [],
    'firewall_group_id': '',
    'gateway_v4': '0.0.0.0',
    'hostname': 'vpn-dfw.cssnr.com',
    'id': '9ec77336-4c3a-4b14-8d73-a3e46652281a',
    'image_id': '',
    'internal_ip': '',
    'kvm': '',
    'label': 'openvpn',
    'main_ip': '0.0.0.0',
    'netmask_v4': '',
    'os': 'Ubuntu 20.04 x64',
    'os_id': 387,
    'plan': 'vc2-1c-1gb',
    'power_status': 'running',
    'ram': 1024,
    'region': 'dfw',
    'server_status': 'none',
    'status': 'pending',
    'tag': 'vpn-dfw.cssnr.com',
    'v6_main_ip': '',
    'v6_network': '',
    'v6_network_size': 0,
    'vcpu_count': 1,
}


@shared_task()
def clear_sessions():
    return management.call_command('clearsessions')


@shared_task()
def create_instance(api_token, location_id):
    logger.debug('api_token: %s', api_token)
    logger.debug('location_id: %s', location_id)

    vultr = Vultr(api_token)

    hostname = f'openvpn-{location_id}.local'

    os_list = vultr.list_os()
    ubuntu_lts = vultr.filter_os(os_list, 'Ubuntu 20.04 x64')

    scripts = vultr.list_scripts()
    script = vultr.filter_scripts(scripts, 'openvpn-bootstrap.sh')
    if not script:
        print('script not found, creating new script...')
        path = os.path.join(settings.STATIC_ROOT, 'scripts', 'openvpn-bootstrap.sh')
        file = open(path, 'r')
        contents = file.read()
        message_bytes = contents.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        script = vultr.create_script('openvpn-bootstrap.sh', base64_message)
    logger.debug(script)

    data = {
        'plan': 'vc2-1c-1gb',
        'region': location_id,
        'os_id': ubuntu_lts['id'],
        'script_id': script['id'],
        'hostname': hostname,
        'label': hostname,
        'tag': 'openvpn',
    }
    logger.debug(data)

    resp = vultr.create_instance(**data)
    return resp


@shared_task()
def delete_instance(api_token, instance_id):
    logger.debug('api_token: %s', api_token)
    logger.debug('instance_id: %s', instance_id)
    vultr = Vultr(api_token)
    vultr.delete_instance(instance_id)
    return None
