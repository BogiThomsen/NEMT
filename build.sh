#!/bin/bash

cd services/core/user
docker-compose build
cd ..
cd device
docker-compose build
cd ..
cd ..
cd data_access/user
docker-compose build
cd ..
cd device
docker-compose build
cd ..
cd sensors
docker-compose build
cd ..
cd ..
cd edge/web_app_api
docker-compose build
cd ..
cd ..
cd ..

