from enum import Enum


class VideoType(str, Enum):
    YOUTUBE = "YOUTUBE"
    INSTAGRAM = "INSTAGRAM"


class FileType(str, Enum):
    XLSX = "xlsx"
    CSV = "csv"
    ALL_FORMAT = "all_format"
