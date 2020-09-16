from dataclasses import dataclass, asdict
from dacite import from_dict


@dataclass
class BezrealitkyBaseApartmentDto:
    id: int = None
    uri: str = None

    @staticmethod
    def from_dict(data: dict) -> 'BezrealitkyBaseApartmentDto':
        data['id'] = int(data['id'])
        return from_dict(BezrealitkyBaseApartmentDto, data)


@dataclass
class Coordinates:
    lat: float = 0.0
    lng: float = 0.0


@dataclass
class BezrealitkyApartmentDTO(BezrealitkyBaseApartmentDto):
    title: str = None
    sub_title: str = None
    coordinates: Coordinates = None
    apartment_info: dict = None

    def asdict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'BezrealitkyApartmentDTO':
        return from_dict(data_class=BezrealitkyApartmentDTO, data=data)
