set -e
unset http_proxy
unset https_proxy
# Workaround for cron, won't work on other systems
export PATH=/usr/local/Caskroom/miniconda/base/condabin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

CONTAINER_NAME=prague-rents-mongo

function clean_up {
  echo "Stopping docker container(s)"
  # add if CID is not empty
  docker-compose -f docker/docker-compose.yml -p prague-rents stop
}
trap clean_up EXIT

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

clean_up
