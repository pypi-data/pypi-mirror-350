from typing import Any, Optional

from supabase import create_client, Client
from boto3.session import Session
from botocore.config import Config
import s3fs

from .config import get_settings


def get_supabase_client(settings_override: Optional[dict[str, Any]] = None) -> Client:
    settings = get_settings(**(settings_override or {}))

    return create_client(
        supabase_url=settings.supabase_url,
        supabase_key=settings.supabase_key
    )

def get_storage_client(settings_override: Optional[dict[str, Any]] = None):
    settings = get_settings(**(settings_override or {}))

    session = Session()
    client = session.client(
        "s3",
        endpoint_url=settings.storage_endpoint_url,
        aws_access_key_id=settings.storage_access_key,
        aws_secret_access_key=settings.storage_secret_key,
        config=Config(signature_version="s3")
        #region_name=settings.storage_region,
    )

    return client

def get_storage_fs(settings_override: Optional[dict[str, Any]] = None):
    settings = get_settings(**(settings_override or {}))

    return s3fs.S3FileSystem(
        endpoint_url=settings.storage_endpoint_url,
        key=settings.storage_access_key,
        secret=settings.storage_secret_key,
        #region_name=settings.storage_region,
    )
