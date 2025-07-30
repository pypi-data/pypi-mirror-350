from ...types import ExternalAsset


class StrategyAsset(ExternalAsset):
    """Strategy assets that can be extracted"""

    ATTRIBUTE = "attribute"
    CUBE = "cube"
    DASHBOARD = "dashboard"
    DOCUMENT = "document"
    FACT = "fact"
    METRIC = "metric"
    REPORT = "report"
    USER = "user"
