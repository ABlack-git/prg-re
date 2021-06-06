from typing import Tuple, Union, List

import requests
import logging
from bs4 import BeautifulSoup
from prague_rents.bezrealitky.entities import Coordinates, BezrealitkyListing, BezrealitkyListingBaseDto
from prague_rents.bezrealitky.enums import ApartmentInfo, info_mapping, layout_mapping

log = logging.getLogger('main')

_BASE_URL = 'https://www.bezrealitky.com'
_API_APARTMENTS_LIST = 'https://www.bezrealitky.cz/api/record/markers'
_FLATS_URL = _BASE_URL + '/properties-flats-houses'


def __make_soup(url) -> BeautifulSoup:
    resp = requests.get(url)
    return BeautifulSoup(resp.content, 'html.parser')


def get_list_of_listings() -> List[BezrealitkyListingBaseDto]:
    request_body = {
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
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post(_API_APARTMENTS_LIST, data=request_body, headers=headers).json()
    return [BezrealitkyListingBaseDto.from_dict(data) for data in resp if data['type'] != 'iDeveloper']


def get_listing(uri: str, listing_id: int) -> BezrealitkyListing:
    listing_page = __make_soup(_FLATS_URL + '/' + uri)
    listing = BezrealitkyListing()
    listing.listing_id = listing_id
    listing.uri = uri
    listing.title, listing.sub_title = _parse_titles(listing_page)
    listing.coordinates = _parse_coords(listing_page)
    listing.info = _parse_info(listing_page)
    return listing


def _parse_coords(page: BeautifulSoup) -> Coordinates:
    map_div = page.find('div', class_='b-map__inner')
    return Coordinates(lat=float(map_div.get('data-lat')), lon=float(map_div.get('data-lng')))


def _parse_titles(page: BeautifulSoup) -> Tuple[str, str]:
    header = page.find('h1', class_='heading__title').find_all('span')
    title = header[0].get_text()
    sub_title = list(header[1].stripped_strings)[0]
    return title, sub_title


def _parse_info(page: BeautifulSoup) -> dict:
    info_table = page.find('table', class_='table').find_all('tr')
    info_dict = {}
    for spec_entry in info_table:
        info_name: str = spec_entry.find('th').get_text().strip(':')
        info_type = info_mapping[info_name] if info_name in info_mapping else None
        value = spec_entry.find('td').get_text()
        if info_type is not None:
            value = __process_info_value(info_type, value)
            info_dict[info_type.key] = value
        else:
            log.warning(f"{info_name} key is not known")
            info_dict[info_name.lower().replace(' ', '_')] = value
    return info_dict


def __process_info_value(info_type: ApartmentInfo, value: str) -> Union[str, int, bool]:
    if info_type.prop_type == str:
        if info_type == ApartmentInfo.LAYOUT:
            return layout_mapping[value]
        return value
    if info_type.prop_type == int:
        if info_type == ApartmentInfo.FLOOR_SPACE:
            return int(value.split(' ')[0])
        elif info_type in (ApartmentInfo.PRICE, ApartmentInfo.FEES, ApartmentInfo.DEPOSIT):
            return int(value.split(' ')[1].replace(',', ''))
        else:
            return int(value)
    elif info_type.prop_type == bool:
        return value.lower() in ('yes', 'true', 'y', 'ano')
