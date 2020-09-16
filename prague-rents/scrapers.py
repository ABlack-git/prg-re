import requests

from bs4 import BeautifulSoup
from .repo import MongoRepository
from .entities import BezrealitkyListing
from urllib.parse import urlparse, parse_qs


class BezrealitkyScraper:
    def __init__(self, repository: MongoRepository):
        self.api_apart_list = 'https://www.bezrealitky.cz/api/record/markers'
        self.base_url = 'https://www.bezrealitky.com/properties-flats-houses/'
        self.repo = repository
        self.api_form_data = {
            'offerType': 'pronajem',
            'estateType': 'byt',
            'boundary': str([[{"lat": 50.0998947, "lng": 14.6911961}, {"lat": 50.0721289, "lng": 14.6999919},
                              {"lat": 50.0568947, "lng": 14.6401916}, {"lat": 50.0188407, "lng": 14.669537},
                              {"lat": 49.9944411, "lng": 14.6401518}, {"lat": 50.0163634, "lng": 14.582393},
                              {"lat": 50.0108381, "lng": 14.5274725}, {"lat": 49.9707711, "lng": 14.4622402},
                              {"lat": 49.9706693, "lng": 14.4006472}, {"lat": 49.9419006, "lng": 14.395562},
                              {"lat": 49.9572087, "lng": 14.3254392}, {"lat": 49.9676279, "lng": 14.344916},
                              {"lat": 49.9718588, "lng": 14.3268138}, {"lat": 49.9906467, "lng": 14.3427236},
                              {"lat": 50.0022104, "lng": 14.2948377}, {"lat": 50.0235957, "lng": 14.3158639},
                              {"lat": 50.0583091, "lng": 14.2480852}, {"lat": 50.0771366, "lng": 14.2893735},
                              {"lat": 50.1029963, "lng": 14.2244355}, {"lat": 50.1300802, "lng": 14.302453},
                              {"lat": 50.1160189, "lng": 14.3607835}, {"lat": 50.1480311, "lng": 14.3657001},
                              {"lat": 50.141429, "lng": 14.3949016}, {"lat": 50.1774301, "lng": 14.5268551},
                              {"lat": 50.1501702, "lng": 14.5632297}, {"lat": 50.1541328, "lng": 14.5990028},
                              {"lat": 50.1452435, "lng": 14.5877286}, {"lat": 50.1293063, "lng": 14.6008738},
                              {"lat": 50.1226041, "lng": 14.6591154}, {"lat": 50.1065008, "lng": 14.657436},
                              {"lat": 50.0998947, "lng": 14.6911961}]]).replace(' ', '').replace("'", '"'),
            'hasDrawnBoundary': 'true',
            'locationInput': 'Praha'
        }

    @staticmethod
    def make_soup(url):
        resp = requests.get(url)
        return BeautifulSoup(resp.content, 'html.parser')

    def get_apartments_list(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.api_apart_list, data=self.api_form_data, headers=headers)
        return response.json()

    def _parse_specs(self, page: BeautifulSoup) -> dict:
        spec_table = page.find('table', class_='table').find_all('tr')
        spec_dict = {}
        for spec_entry in spec_table:
            key = spec_entry.find('th').get_text().strip(':')
            value = spec_entry.find('td').get_text()
            spec_dict[key] = value
        return spec_dict

    def _parse_coords(self, page: BeautifulSoup) -> str:
        link_with_coords = page.find('div', class_='b-map').find('iframe').get('src')
        parsed_link = urlparse(link_with_coords)
        link_query = parse_qs(parsed_link.query)
        return link_query['q'][0]

    def _parse_headers(self, page: BeautifulSoup):
        header = page.find('h1', class_='heading__title').find_all('span')
        title = header[0].get_text()
        sub_title = list(header[1].stripped_strings)[0]
        return title, sub_title

    def scrap_listing(self, uri: str, listing_id: str) -> BezrealitkyListing:
        listing_page = self.make_soup(self.base_url + uri)

        listing = BezrealitkyListing()
        listing.uri = uri
        listing.listing_id = int(listing_id)
        listing.specs = self._parse_specs(listing_page)
        listing.coords = self._parse_coords(listing_page)
        listing.title, listing.sub_title = self._parse_headers(listing_page)
        return listing

    def scrap(self):
        apart_list = self.get_apartments_list()
        for apart_obj in apart_list:
            listing = self.scrap_listing(apart_obj['uri'], apart_obj['id'])
            self.repo.insert_one(BezrealitkyListing.COLLECTION, listing.get_document())

