

from enum import Enum


class APPLIANCES(Enum):
    TV = "TV"
    AIR_CONDITIONER = "Air Conditioner"
    DISH_WASHER = "Dish Washer"
    ELECTRIC_OVEN = "Electric Oven"
    MICROWAVE = "Microwave"
    WASHING_MACHINE = "Washing Machine"
    CLOTHES_DRYER = "Clothes Dryer"
    FRIDGE = "Fridge"
    OTHER = "Other"


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

TZ_FRANCE_NAME = 'Europe/Paris'
TZ_ROMANIA_NAME = 'Europe/Bucharest'
