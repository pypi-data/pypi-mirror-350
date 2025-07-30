from enum import Enum


class DbcanAnnotationType(str, Enum):
    EC_NUMBER = "EC_NUMBER"
    DOMAIN = "DOMAIN"
