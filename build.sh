#!/bin/bash

cd services/core/user
docker-compose build --no-cache
cd ..
cd device
docker-compose build --no-cache
cd ..
cd sensor
docker-compose build --no-cache
cd ..
cd action
docker-compose build --no-cache
cd ..
cd ..
cd data_access/user
docker-compose build --no-cache
cd ..
cd device
docker-compose build --no-cache
cd ..
cd sensors
docker-compose build --no-cache
cd ..
cd actions
docker-compose build --no-cache
cd ..
cd ..
cd edge/web_app_api
docker-compose build --no-cache
cd ..
cd device_api
docker-compose build --no-cache
cd ..
cd edge/web_app
docker-compose build
cd ..
cd ..
cd ..

