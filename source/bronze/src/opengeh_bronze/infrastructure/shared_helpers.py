def get_storage_base_path(
    storage_account_name: str,
    container_name: str,
) -> str:
    return f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/"


def get_checkpoint_path(
    datalake_storage_account_name: str,
    container_name: str,
    table_name: str,
) -> str:
    return get_storage_base_path(datalake_storage_account_name, container_name) + f"checkpoints/{table_name}"
