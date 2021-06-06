import logging.config
import logging
from mongoengine import connect
from prague_rents.bezrealitky import scraper
import yaml

with open('logger-conf.yml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
log = logging.getLogger('main')


def read_config():
    with open('config.yml', 'r') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf


def main():
    log.info("Starting scraper")
    config = read_config()
    connect(config['mongo']['database'], host=config['mongo']['host'], port=config['mongo']['port'])
    scraper.scrap()


if __name__ == '__main__':
    main()
