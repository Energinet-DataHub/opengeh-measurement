from pydantic_settings import SettingsConfigDict

from opengeh_electrical_heating.application.job_args.electrical_heating_args import ElectricalHeatingArgs


class ElectricalHeatingTestArgs(ElectricalHeatingArgs):
    """Args for testing the electrical heating job."""

    def __init__(self, env_file_path: str) -> None:
        """
        Class inherits from ElectricalHeatingJobArgs by overriding the constructor and setting a specific path for
        the environment file provided in the scenario tests with parameter env_file
        """
        self.__class__.model_config = SettingsConfigDict(env_file=env_file_path)
        super().__init__()
