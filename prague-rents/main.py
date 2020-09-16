import yaml

from repo import MongoRepository
from scrapers import BezrealitkyScraper


def read_config():
    with open('config.yml', 'r') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf


if __name__ == '__main__':
    config = read_config()
    mongo_conf = config['mongo']
    repo = MongoRepository(mongo_conf['host'], mongo_conf['port'], mongo_conf['database'])
    bezr_scraper = BezrealitkyScraper(repo)
    bezr_scraper.scrap()
