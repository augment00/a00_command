from crypt import crypt
from fabric.api import local, settings, abort, run, env, sudo, put, get, prefix, cd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from config_local import PI_PASSWORD

env.hosts = ["%s:%s" % ("raspberrypi.local", 22)]
# env.hosts = ["%s:%s" % ("169.254.162.179", 22)]
env.user = "pi"
env.password = PI_PASSWORD


COMMAND_VERSION = "0.0.1"


############################################################################
##              Push code to card for dev                       ##
############################################################################
"""
On the pi stop the default containers from running:

cd /etc/opt/augment00
docker-compose stop

Then push the code with the command update below and run using the dev compose script:

cd /opt/augment00/dev
docker-compose up/start/stop etc as normal

"""

def update():
    sudo("mkdir -p /opt/augment00/dev")
    sudo("mkdir -p /opt/augment00/dev/command")
    put("../src/a00_command", "/opt/augment00/dev/command", use_sudo=True)
    put("../main.py", "/opt/augment00/dev/command", use_sudo=True)
    put("docker-compose-dev.yml", "/opt/augment00/dev/docker-compose.yml", use_sudo=True)
    put(".env", "/opt/augment00/dev/.env", use_sudo=True)

