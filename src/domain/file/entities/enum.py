from enum import Enum


class ContentType(Enum):

    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    WEBP = "image/webp"
    BMP = "image/bmp"
    SVG = "image/svg+xml"
    TIFF = "image/tiff"

    PDF = "application/pdf"
    DOC = "application/msword"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    XLS = "application/vnd.ms-excel"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    PPT = "application/vnd.ms-powerpoint"
    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    TXT = "text/plain"
    CSV = "text/csv"
    JSON = "application/json"
    XML = "application/xml"

    ZIP = "application/zip"
    GZIP = "application/gzip"
    TAR = "application/x-tar"
    RAR = "application/vnd.rar"
    _7Z = "application/x-7z-compressed"

    MP4 = "video/mp4"
    MPEG = "video/mpeg"
    OGG_VIDEO = "video/ogg"
    MP3 = "audio/mpeg"
    OGG_AUDIO = "audio/ogg"
    WAV = "audio/wav"
    WEBM = "video/webm"
    AVI = "video/x-msvideo"

    HTML = "text/html"
    CSS = "text/css"
    JS = "application/javascript"
    ICO = "image/vnd.microsoft.icon"

    @classmethod
    def to_dict(cls) -> dict:
        return {data.name: data.value for data in cls}
