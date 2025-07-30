from enum import Enum

class MultiplatformType(str, Enum):
    JVM = 'JVM'
    NATIVE = 'NATIVE'
    JS = 'JS'
