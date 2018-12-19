# NEMT

First edit the url in the top of web_app/app/main.py, to the ip your docker containers are exposed at.

To run the platform on linux:
- have docker and docker compose installed.
- modify services/nginx.conf and put the IPs of the machines you want to run the containers on in the upstream.
- If running on multiple machines, comment out the nginx service in services/docker-compose.yml
- run ./build
- run ./up
- visit localhost.

To run the platform on Windows:
- have docker and docker compose installed
- modify web-app/main.py to request to the IP your docker machine is exposed at.
- modify services/nginx.conf and put the IPs of the machines you want to run the containers on in the upstream.
- If running on multiple machines: on the slave machines, comment out the nginx service in services/docker-compose.yml
- run ./build
- run ./up
- visit the IP your docker machine is exposed at.