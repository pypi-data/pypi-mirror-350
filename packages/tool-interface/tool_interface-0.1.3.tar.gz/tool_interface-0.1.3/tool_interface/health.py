"""Health check utilities for tool-interface connections."""

from typing import Any, Optional

from boto3.session import Session
from botocore.exceptions import ClientError
from supabase import Client, create_client

from .config import get_settings
from ._connections import get_supabase_client, get_storage_client

# Current version of the tool-interface package
# This should match the latest schema version in Supabase
MAXIMUM_SUPPORTED_SCHEMA_VERSION = 1
MINIMUM_SUPPORTED_SCHEMA_VERSION = 1


def check_supabase_connection(
    settings_override: Optional[dict[str, Any]] = None,
) -> tuple[bool, str]:
    """
    Check if Supabase connection is working and schema version matches.

    Args:
        settings_override: Optional dictionary to override settings.

    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        client = get_supabase_client(settings_override)

        # Try to get the current schema version
        response = client.table("_schema_version").select("*").order("applied_at", desc=True).limit(1).execute()
        if not response.data:
            return (
                False,
                "Schema version table exists but no version found. Database might not be initialized.",
            )

        current_version = response.data[0]["version"]
        if current_version < MINIMUM_SUPPORTED_SCHEMA_VERSION:
            return (
                False,
                f"Schema version mismatch. Expected at least {MINIMUM_SUPPORTED_SCHEMA_VERSION}, found {current_version}."
                + " You are missing supabase migrations.",
            )
        if current_version > MAXIMUM_SUPPORTED_SCHEMA_VERSION:
            return (
                False,
                f"Schema version mismatch. Expected at most {MAXIMUM_SUPPORTED_SCHEMA_VERSION}, found {current_version}."
                + " You need to update tool-interface: pip install --upgrade tool-interface",
            )
        return (
            True,
            f"Successfully connected to Supabase (schema version {current_version})",
        )
    except Exception as e:
        if "does not exist" in str(e):
            return (
                False,
                "Schema version table not found. Database might not be initialized.",
            )
        return False, f"Failed to connect to Supabase: {str(e)}"


def check_storage_connection(
    settings_override: Optional[dict[str, Any]] = None,
) -> tuple[bool, str]:
    """
    Check if GCS/S3 connection is working.

    Args:
        settings_override: Optional dictionary to override settings.

    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        settings = get_settings(**(settings_override or {}))
        s3_client = get_storage_client(settings_override)

        # Try to list objects to verify connection
        s3_client.head_bucket(Bucket=settings.storage_bucket_name)

        return True, "Successfully connected to storage"
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        if error_code == "403":
            return False, "Access denied to storage bucket. Check credentials."
        elif error_code == "404":
            return False, "Storage bucket not found."
        return False, f"Failed to connect to storage: {str(e)}"
    except Exception as e:
        return False, f"Failed to connect to storage: {str(e)}"


def check_all_connections(
    settings_override: Optional[dict[str, Any]] = None,
) -> dict[str, dict[str, str]]:
    """
    Check all connections and return their status.

    Args:
        settings_override: Optional dictionary to override settings.

    Returns:
        Dict with status of all connections
    """
    supabase_success, supabase_msg = check_supabase_connection(settings_override)
    storage_success, storage_msg = check_storage_connection(settings_override)

    return {
        "supabase": {
            "status": "healthy" if supabase_success else "unhealthy",
            "message": supabase_msg,
        },
        "storage": {
            "status": "healthy" if storage_success else "unhealthy",
            "message": storage_msg,
        },
    }
