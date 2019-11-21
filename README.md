# JupyterHub deployment for Deep Learning containing famous Data Science / Deep Learning libs + CUDA GPU support

This is an adapted version of the [Jupyterhub](https://jupyter.org/hub) deployment in use at the Uni of Konstanz based on the
deployment in use at [Université de
Versailles](https://jupyter.ens.uvsq.fr/).

## Features

- Containerized single user Jupyter servers, using
  [DockerSpawner](https://github.com/jupyterhub/dockerspawner);
- Authentication via PAM
- Singleuser-Image containing popular Data Science/Deep Learning libs + CUDA with GPU support
- User data persistence;
- HTTPS proxy.

## Learn more

This deployment is described in depth in [this blog
post](https://opendreamkit.org/2018/10/17/jupyterhub-docker/).

### Understand the basic configuration

This deployment is ready to clone and roll on your own server. Read
the [blog
post](https://opendreamkit.org/2018/10/17/jupyterhub-docker/) first,
to be sure you understand the configuration.

### How to configure for your needs

0. Make sure your servers runs [nvidia-docker](https://github.com/NVIDIA/nvidia-docker)
1. Adjust `HOST` variable in [`.env`](.env) to the name of your server
2. In [`reverse-proxy/traefik.toml`](reverse-proxy/traefik.toml), edit
  the paths in `certFile` and `keyFile` and point them to your own TLS
  certificates. Possibly edit the `volumes` section in the
  `reverse-proyx` service in
  [`docker-compose.yml`](docker-compose.yml).
3. Add the group `jupyterhubuser` to the system and add all users allowed to authenticate + maybe adjust admin user in [jupyterhub_config](jupyterhub/jupyterhub_config.py) (default user is `sysadmin`):
```
sudo groupadd jupyterhubuser
# for each allowed user run
sudo usermod -a -G jupyterhubuser $user
```
4. Build the image and deploy
```
docker-compose build
docker-compose up -d
```

5. Execute `update_users.sh` to dynamically add the users for PAM authentication (see https://github.com/jupyterhub/jupyterhub/issues/535#issuecomment-267571563):
```
bash update_users.sh
```

6. In case you exposed the deployment to a public ip address, adjust the firewall rules:

```
# Execute iptables -S
iptables -S

# Look for rules that look similar to be following (having just different ports 80/443/8080 respectively)
# -A DOCKER -d 172.31.0.3/32 ! -i br-48fc30176f0a -o br-48fc30176f0a -p tcp -m tcp --dport 80 -j ACCEPT
# Remove these rules:
iptables -D DOCKER -d 172.31.0.3/32 ! -i br-48fc30176f0a -o br-48fc30176f0a -p tcp -m tcp --dport 80 -j ACCEPT

# Add -s ip/range to the rules to restrict access
iptables -I -s x.x.x.x/16 DOCKER -d 172.31.0.3/32 ! -i br-48fc30176f0a -o br-48fc30176f0a -p tcp -m tcp --dport 80 -j ACCEPT

```

Other changes you may like to make:

- Edit [`jupyterlab/Dockerfile`](jupyterlab/Dockerfile) to include the
  software you like. Do not forget to change
  [`jupyterhub/jupyterhub_config.py`](jupyterhub/jupyterhub_config.py)
  accordingly, in particular the *"user data persistence"* section.
  **NOTE**: When making changes to [`jupyterhub/jupyterhub_config.py`](jupyterhub/jupyterhub_config.py), make sure to delete the volume containing the config before rebuild: `docker volume rm jupyterhub_jupyterhub_data`

Other useful information:

- Whenever you add a new user, you can just execute `bash update_uesrs.sh` to dynamically add the new user to the deployment.
- [NodeJS](https://nodejs.org/en/) is installed to the image, so in jupyterlab the extension manager is available for any user to install further jupyterlab extensions
- The singleuser images are configures to be removed automatically after 365 days of inactivity, change the `--timeout=number` in the section  `c.JupyterHub.services` of [`jupyterhub/jupyterhub_config.py`](jupyterhub/jupyterhub_config.py) in case you want to change that
- The users are able to add own virtual environments, the following commands show how to add an environments using already installed packages, make it persistent by installing it in the users home directory and to add it as a new ipython kernel to start notebooks via the virtual environment:
```
## Init conda ##
conda init bash
exec bash

## Create new conda environment using all already install packages ##
## and add an example package                                      ##
# Create env (using all already installed packages => --clone base)
conda create --prefix=$name --clone base
# Activate new env
conda activate $HOME/name
# Install new packages, here e.g. upgrade to tensorflow 2.0
pip install tensorflow-gpu
# Add the new environment as a new ipython kernel to be able to start notebooks from it
ipython kernel install --user --name=$name 
# deactivate env
conda deactivate

# remove an env
conda env remove --p $HOME/$name
```


## Acknowledgements

The major part of the work for this deployment was already done by Université de Versailles (see forked repo) and a lot of the content of the singleuser-image is copied over from other images. See comments in the [Dockerfile](jupyterlab/dockerfile).
