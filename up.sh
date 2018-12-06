#!/bin/bash

docker network create --driver bridge platform

cd services/edge/web_app_api
docker-compose up -d
cd ..
cd ..
cd core/user
docker-compose up -d
cd ..
cd ..
cd data_access/user
docker-compose up -d