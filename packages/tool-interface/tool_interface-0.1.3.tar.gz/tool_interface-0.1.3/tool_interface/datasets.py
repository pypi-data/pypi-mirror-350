from typing import Any, Optional

from .models import LASMetadata, Dataset
from ._connections import get_supabase_client
from .config import get_settings


def get_dataset(dataset_id: Optional[int] = None, object_name: Optional[str] = None, settings_override: Optional[dict[str, Any]] = None, load_las_metadata: bool = True) -> Dataset:
    dataset_record = _get_dataset_record(dataset_id, object_name, settings_override)
    if load_las_metadata:
        las_metadata = _load_las_metadata(dataset_record, settings_override)
        dataset_record.las_metadata = las_metadata

    return dataset_record


def _get_dataset_record(dataset_id: Optional[int] = None, object_name: Optional[str] = None, settings_override: Optional[dict[str, Any]] = None) -> Dataset:
    if dataset_id is None and object_name is None:
        raise ValueError("Either dataset_id or dataset_name must be provided")
    if dataset_id is not None and object_name is not None:
        raise ValueError("Only one of dataset_id or dataset_name can be provided")
    
    settings = get_settings(**(settings_override or {}))
    client = get_supabase_client(settings_override=settings_override)

    if dataset_id is not None:
        response = client.table(settings.datasets_table).select("*").filter("id", "eq", dataset_id).execute()
    elif object_name is not None:
        response = client.table(settings.datasets_table).select("*").filter("object_name", "eq", object_name).execute()
    
    if len(response.data) == 0:
            raise ValueError(f"Dataset with id {dataset_id} not found")
    elif len(response.data) > 1:
        raise ValueError(f"Multiple datasets with id {dataset_id} found")

    dataset = Dataset(**response.data[0])
    dataset._settings = settings
    return dataset

def _load_las_metadata(dataset: Dataset, settings_override: Optional[dict[str, Any]] = None) -> LASMetadata:
    settings = get_settings(**(settings_override or {}))
    client = get_supabase_client(settings_override=settings_override)
     
    response = client.table(settings.las_metadata_table).select("*").filter("dataset_id", "eq", dataset.id).execute()

    if len(response.data) == 0:
        raise ValueError(f"No LAS metadata found for dataset {dataset.id}")
    elif len(response.data) > 1:
        raise ValueError(f"Multiple LAS metadata records found for dataset {dataset.id}")
    
    return LASMetadata(**response.data[0])


