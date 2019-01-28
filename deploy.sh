#! /bin/sh

source <(cat .env | sed -e "s+^\([^# ]\)+export \1+g")
# export DOCKER_HOST=tcp://ymslanda.innovationgarage.tech:2375

docker build --tag ${REPO}elcheapoais_cartogateway:latest cartogateway
docker push ${REPO}elcheapoais_cartogateway:latest

docker build --tag ${REPO}elcheapoais_concentrator:latest concentrator
docker push ${REPO}elcheapoais_concentrator:latest

docker build --tag ${REPO}elcheapoais_cartodb:latest cartodb
docker push ${REPO}elcheapoais_cartodb:latest

docker build --tag ${REPO}elcheapoais_manhole:latest git@github.com:innovationgarage/ElCheapoAIS-manhole.git
docker push ${REPO}elcheapoais_manhole:latest

docker stack deploy -c docker-compose.yml elcheapoais
