from ed_domain.core.entities.base_entity import BaseEntity


class Car(BaseEntity):
    make: str
    model: str
    year: int
    registration_number: str
    license_plate_number: str
    color: str
    seats: int
