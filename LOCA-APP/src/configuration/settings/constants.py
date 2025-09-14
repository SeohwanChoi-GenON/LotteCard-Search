class UvicornConfig:
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    LOG_LEVEL: str = "info"
    TIMEOUT_KEEP_ALIVE: int = 30


class ServiceIds:
    UNIFIED = "Unified"
    CARD = "Card"
    EVENT = "Event"
    CONTENTS = "Contents"
    COMMERCE = "Commerce"
    MENU = "Menu"


class IntentTypes:
    FAQ = "FAQ"
    VDB = "VDB"
    REQUERY = "재질의"


class VDBIndexes:
    CARD = "Card"
    EVENT = "Event"
    CONTENT = "Content"