import logging
import bezrealitky.client as client
from time import sleep
from bezrealitky.entities import BezrealitkyListing

log = logging.getLogger('main')


def scrap():
    log.info('Starting bezrealitky scraper')
    list_of_listings = client.get_list_of_listings()
    log.info(f'Found {len(list_of_listings)} listings')
    set_of_listing_ids = _update_inactive({l.id for l in list_of_listings})
    filtered_list = [l for l in list_of_listings if l.id in set_of_listing_ids]
    log.info(f'After filtering {len(filtered_list)} listings remained')

    for base_listing in filtered_list:
        sleep(1)
        log.info(f'Scraping listing with id: {base_listing.id} uri: {base_listing.uri}')
        listing = client.get_listing(base_listing.uri, base_listing.id)
        listing.save()

    log.info("Finished scraping bezrealitky")


def _update_inactive(listing_ids: set):
    active_listings = BezrealitkyListing.objects(active=True).only('listing_id')
    for listing in active_listings:
        if listing.listing_id not in listing_ids:
            BezrealitkyListing.objects(listing_id=listing.listing_id).update(set__active=False)
        else:
            listing_ids.remove(listing.listing_id)
    return listing_ids
