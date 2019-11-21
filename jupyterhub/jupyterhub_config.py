# JupyterHub configuration
#
## If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
##
##     docker volume rm jupyterhub_jupyterhub_data
##
## or, if you changed the COMPOSE_PROJECT_NAME to <name>:
##
##    docker volume rm <name>_jupyterhub_data
##

import os

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

## Authentication

c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'


# Make the Jupyterhub accessible

c.NotebookApp.allow_origin = '*' # make it accessible from the outside world
c.NotebookApp.ip = os.environ['IP']

## Authenticator

c.LocalAuthenticator.group_whitelist = {'jupyterhubuser'}
c.Authenticator.admin_users = { 'sysadmin' }


## Docker spawner
#c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.spawner_class = 'dockerspawner.SystemUserSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
#notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
notebook_dir = '/home/{username}'
c.DockerSpawner.notebook_dir = notebook_dir

# Other stuff
#c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '20G'


# Remove containers when they are stopped
c.DockerSpawner.remove_containers = True

## Services
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python /srv/jupyterhub/cull_idle_servers.py --timeout=31536000'.split(),
    },
]
