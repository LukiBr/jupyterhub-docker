#!bin/bash

docker exec -it jupyterhub bash -c "cp -f /jup_etc/passwd /etc/passwd; cp -f /jup_etc/shadow /etc/shadow; cp -f /jup_etc/group /etc/group"
