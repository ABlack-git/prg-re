import json


class BezrealitkyListing:
    COLLECTION = 'bezrealitky'

    def __init__(self):
        self.listing_id = None
        self.uri = None
        self.title = None
        self.sub_title = None
        self._specifications = None
        self._coordinates = None

        self.__layout_mapping = {
            'Small studio': 'Garsoniera',
            'Studio': '1kk',
            '1 bedroom': '1+1',
            '1 bedroom with open-plan kitchen': '2+kk',
            '2 bedroom': '2+1',
            '2 bedroom with open-plan kitchen': '3+kk',
            '3 bedroom': '3+1',
            '3 bedroom with open-plan kitchen': '4+kk',
            '4 bedroom': '4+1',
            '4 bedroom with open-plan kitchen': '5+kk',
            '5 bedroom': '5+1',
            '5 bedroom with open-plan kitchen': '5+kk',
            '6 bedroom': '6+1',
            '6 bedroom with open-plan kitchen': '7+kk',
            '7 bedroom': '7+1',
            'Other': 'Other'
        }
        self.__LAYOUT = 'Layout'
        self.__PRICE = 'Price'
        self.__FEES = 'Fees'
        self.__DEPOSIT = 'Refundable security deposit'
        self.__FLOOR_SPACE = 'Floor Space'

    @property
    def coords(self):
        return self._coordinates

    @coords.setter
    def coords(self, value: str):
        coords_list = value.split(',')
        assert len(coords_list) == 2
        self._coordinates = {
            'lat': float(coords_list[0]),
            'lng': float(coords_list[1])
        }

    @property
    def specs(self):
        return self._specifications

    @specs.setter
    def specs(self, value: dict):
        self._specifications = value
        if self.__LAYOUT in self._specifications:
            self._specifications[self.__LAYOUT] = self.__layout_mapping[self._specifications[self.__LAYOUT]]
        if self.__FLOOR_SPACE in self._specifications:
            self._specifications[self.__FLOOR_SPACE] = float(self._specifications[self.__FLOOR_SPACE].split(' ')[0])
        for key in (self.__PRICE, self.__FEES, self.__DEPOSIT):
            if key in self._specifications:
                self._specifications[key] = self._format_price(self._specifications[key])

    @staticmethod
    def _format_price(price: str) -> float:
        return float(price.split(' ')[1].replace(',', ''))

    def get_document(self):
        document = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_' + BezrealitkyListing.__name__):
                k = k.strip('_')
                k = ''.join([x if i == 0 else x.capitalize() for i, x in enumerate(k.split('_'))])
                document[k] = v
        return document

    def __str__(self):
        return json.dumps(self.get_document(), indent=2)
