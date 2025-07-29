import enum

class IndexMode(enum.Enum):
    CHUNCKED = "chunked"
    COMPLETE = "complete"

class MergeChunksMode(enum.Enum):
    AVERAGE = "average"
    MAX = "max"
    MIN = "min"
    SUM = "sum"