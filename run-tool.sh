set -e
unset http_proxy
unset https_proxy

CONTAINER_NAME=prague-rents-mongo

## create/update env
if [[ ! -d .env ]]; then
  echo "Creating conda environment"
  make create-env
#else
#  echo "Updating conda environment"
#  make update-env
fi

## activate env
echo "Activating conda environment"
eval "$(conda shell.bash hook)"
conda activate ./.env

## install package
echo "Installing downloader tool"
make install-e

## start docker
CID=$(docker ps -q -f status=running -f name=${CONTAINER_NAME})
if [[ -z ${CID} ]]; then
  echo "Launching docker container"
  docker-compose -f docker/docker-compose.yml -p prague-rents up -d
  echo "I will sleep for 10 seconds now"
  sleep 10
  echo "Resuming"
  CID=$(docker ps -q -f status=running -f name=${CONTAINER_NAME})
  echo "Docker container was started with ID ${CID}"
else
  echo "Docker container ${CONTAINER_NAME} was running with ID ${CID}"
fi

## start tool
echo "Starting tool"
prg-rents-downloader