from pydantic_settings import BaseSettings


class StorageAccountSettings(BaseSettings):
    """Configuration class inheriting pydantic's BaseSettings to automatically load environmental variable.

    Used to define and validate settings for connecting to the submitted transactions Event Hub.

    Attributes:
    DATALAKE_STORAGE_ACCOUNT (str): The name of the Data Lake storage account.

    Config:
    case_sensitive (bool): Indicates whether the settings are case-sensitive. Defaults to False.
    """

    DATALAKE_STORAGE_ACCOUNT: str

    class Config:
        case_sensitive = False
