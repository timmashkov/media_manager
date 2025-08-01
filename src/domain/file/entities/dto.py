from dataclasses import asdict, dataclass


@dataclass
class FileMetadata:
    object_name: str
    full_path: str
    bucket: str
    content_type: str
    extension: str

    def to_dict(self) -> dict:
        return {k: str(v) for k, v in asdict(self).items()}
