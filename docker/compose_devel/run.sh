
mkdir -p ../../../../../../data/gogs
docker-machine start default
#docker-machine regenerate-certs default
eval $(docker-machine env default)
docker-compose pull
docker-compose up


