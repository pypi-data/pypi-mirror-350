from enum import Enum

class ControlResellConnectorEnvironment(str, Enum):
    PRODUCTION = 'PRODUCTION'
    STAGING = 'STAGING'
    DEV = 'DEV'
