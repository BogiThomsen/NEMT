#!/bin/bash

docker network create --driver bridge platform

cd services
docker-compose up -d
cd ..
cd web_app
docker-compose up -d
