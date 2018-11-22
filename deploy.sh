#! /bin/sh

source <(cat .env | sed -e "s+^\([^# ]\)+export \1+g")
export DOCKER_HOST=tcp://ymslanda.innovationgarage.tech:2375

docker build --tag ymslanda.innovationgarage.tech:5000/elcheapoais_cartogateway:latest cartogateway
docker push ymslanda.innovationgarage.tech:5000/elcheapoais_cartogateway:latest

docker build --tag ymslanda.innovationgarage.tech:5000/elcheapoais_concentrator:latest concentrator
docker push ymslanda.innovationgarage.tech:5000/elcheapoais_concentrator:latest

docker stack deploy -c docker-compose.yml elcheapoais
