import os
from typing import Any, Set, List
from functools import lru_cache

from ..log import footprint


__all__ = (
    'Env',
)


class Env:
    _allowed_variables: Set[str] = set()

    @staticmethod
    def load_file(file_path: str, override: bool = False, fail_on_missing: bool = False):
        if not os.path.exists(file_path):
            if fail_on_missing:
                raise FileNotFoundError(f"The file {file_path} does not exist.")

            return

        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    key = key.strip().upper()
                    value = value.strip()
                    if key in Env._allowed_variables:
                        if override or key not in os.environ:
                            os.environ[key] = value
                    else:
                        footprint.leave(
                            log_type='warning',
                            message=f"Skipping unallowed environment variable {key}.",
                            controller="Env.load_file",
                            subject=f'Unallowed Environment Variable',
                        )

    @staticmethod
    def register(variables: List[str] | Set[str]):
        Env._allowed_variables.update([item.upper() for item in variables])

    @staticmethod
    @lru_cache(maxsize=128)
    def get(key: str, default: Any = None):
        return os.getenv(key.upper()) or default
