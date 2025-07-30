import os
from os import getcwd, getenv

from duckdi.utils import read_toml


class InjectionsPayload:
    def load(self) -> dict[str, str]:
        """
        Loads the injection configuration from a TOML file defined by the INJECTIONS_PATH
        environment variable, or falls back to ./injections.toml.

        Returns:
            dict[str, str]: A dictionary mapping interface keys to adapter class names.

        Raises:
            FileNotFoundError: If the file does not exist.
            tomllib.TOMLDecodeError: If the file is not a valid TOML.
        """
        injections_path = getenv(
            "INJECTIONS_PATH", os.path.join(getcwd(), "injections.toml")
        )
        return read_toml(injections_path)["injections"]
