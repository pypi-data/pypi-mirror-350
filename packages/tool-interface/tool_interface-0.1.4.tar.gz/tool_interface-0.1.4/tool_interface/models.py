from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from pydantic import UUID4
from datetime import datetime
from enum import StrEnum

from .storage import download_file
from .config import Settings

class Platform(StrEnum):
    ULS = "ULS"
    TLS = "TLS"
    MLS = "MLS"

class LASMetadata(BaseModel):
    id: int
    size_mb: int
    checksum: Optional[str] = None
    location: Optional[str] = None
    bbox: Optional[str] = None
    thumbnail: Optional[str] = None
    overviews: Optional[str] = None
    area: Optional[float] = None

class Dataset(BaseModel):
    _settings: Optional[Settings] = None
    id: int
    uuid: UUID4
    title: str
    bucket_prefix: str
    object_name: str
    platform: Platform
    sensor: str
    terrain_normalized: bool
    scan_pattern: str
    is_preprocessed: bool
    created_at: datetime
    user_id: UUID4
    sensor: Optional[str] = None
    annotation_definition: Optional[str] = None
    forest_type: Optional[str] = None
    las_metadata: Optional[LASMetadata] = None

    @property
    def source_path(self) -> Path:
        return Path(self.bucket_prefix) / self.object_name
    
    def download_las(self, target_dir: str = '.') -> Path:
        if self._settings is None:
            settings = {}
        else:
            settings = self._settings.model_dump()
        return download_file(name=self.object_name, prefix=self.bucket_prefix, target=target_dir, settings_override=settings)


