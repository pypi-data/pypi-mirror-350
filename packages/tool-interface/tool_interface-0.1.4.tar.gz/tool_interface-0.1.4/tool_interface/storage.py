from typing import Optional, Any
from pathlib import Path
import logging as logger

from ._connections import get_storage_client, get_storage_fs
from .config import get_settings

#logger = logging.getLogger(__name__)

def has_file(name: str, prefix: str = 'LAS', settings_override: Optional[dict[str, Any]] = None) -> bool:
    settings = get_settings(**(settings_override or {}))
    fs = get_storage_fs(settings_override=settings_override)

    BASE = Path(settings.storage_bucket_name) / prefix
    return fs.exists(str(BASE / name))


def download_file(name: str, prefix: str = 'LAS', target: str = ".", settings_override: Optional[dict[str, Any]] = None) -> Path:
    settings = get_settings(**(settings_override or {}))
    logger.debug(f"Settings: {settings}")
    fs = get_storage_fs(settings_override=settings_override)

    BASE = Path(settings.storage_bucket_name) / prefix
    path = BASE / name
    
    if not fs.exists(str(path)):
        logger.debug(f"BASE: {BASE}, path: {path}, fs: {fs}")
        raise FileNotFoundError(f"File {path} not found")
    
    target = Path(target)
    if not target.is_dir():
        target = target.parent

    fs.download(str(path), str(target))

    return target / path.name

def upload_single_file(source: str, name: str, prefix: str = 'LAS', settings_override: Optional[dict[str, Any]] = None):
    settings = get_settings(**(settings_override or {}))
    fs = get_storage_fs(settings_override=settings_override)

    BASE = Path(settings.storage_bucket_name) / prefix
    source = Path(source)
    if not source.is_file():
        raise ValueError(f"Source {source} is not a file.")
    
    path = BASE / name
    fs.upload(str(source), str(path))

    return path

def upload_single_file_r(source: str, name: str, prefix: str = 'LAS', settings_override: Optional[dict[str, Any]] = None):
    settings = get_settings(**(settings_override or {}))
    client = get_storage_client(settings_override=settings_override)

    source = Path(source).resolve()
    if not source.is_file():
        raise ValueError(f"Source {source} is not a file.")
    
    #object_name = Path(prefix) / name
    #client.upload_file(str(source), settings.storage_bucket_name, str(object_name))
    if prefix != "":
        object_name = f"{prefix}/{name}"
    else:
        object_name = name
    client.put_object(
        Bucket=settings.storage_bucket_name,
        Key=str(object_name),
        Body=source.read_bytes()
    )

    return object_name