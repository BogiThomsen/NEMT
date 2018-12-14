#!/bin/bash

docker network create --driver bridge platform

cd services/edge/web_app_api
docker-compose up -d
cd ..
cd services/edge/web_app
docker-compose up -d
cd ..
cd device_api
docker-compose up -d
cd ..
cd ..
cd core/user
docker-compose up -d
cd ..
cd device
docker-compose up -d
cd ..
cd sensor
docker-compose up -d
cd ..
cd action
docker-compose up -d
cd ..
cd ..
cd data_access/user
docker-compose up -d
cd ..
cd device
docker-compose up -d
cd ..
cd sensors
docker-compose up -d
cd ..
cd actions
docker-compose up -d