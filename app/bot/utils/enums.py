from enum import Enum


class VideoType(Enum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"


class FileType(Enum):
    XLSX = "xlsx"
    CSV = "csv"
    ALL_FORMAT = "all_format"
