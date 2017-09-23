from charms.reactive import when, when_not, set_state
from charmhelpers.core import hookenv
import subprocess


@when('config.changed.hostname')
def update_hostname():
    config = hookenv.config()
    if config['hostname'] == "$UNIT":
        hostname = hookenv.local_unit().replace('/', '-')
    else:
        hostname = config['hostname']
    if hostname is not "":
        with open('/etc/hostname', 'w') as file:
            file.write(hostname)
        subprocess.call(['hostname', hostname])
        subprocess.check_call(['dhclient', '-r'])
        subprocess.check_call(['dhclient'])
        # TODO Need to replace /etc/hosts line as well
 

@when_not('layer-hostname.installed')
def install_layer_hostname():
    update_hostname()
    set_state('layer-hostname.installed')


