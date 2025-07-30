from wavesql import AsyncWaveSQL
from typing import Literal
from datetime import datetime
from pathlib import Path


class DataBase(AsyncWaveSQL):
    def __init__(
        self, config: dict | str | None = None, path_to_sql: Path | str | None = None,
        is_dictionary: bool = True, is_console_log: bool = False, is_log_backtrace: bool = False,
        raise_log_on_fail: bool = False, is_pprint: bool = False, is_protected: bool = True,
        is_auto_start: bool = False, is_try_update_db: bool = False, is_create_python_bridge: bool = False,
        is_try_update_python_bridge: bool = True
    ) -> None:
        super().__init__(
            config, path_to_sql, is_dictionary, is_console_log, is_log_backtrace,
            raise_log_on_fail, is_pprint, is_protected, is_auto_start, is_try_update_db,
            is_create_python_bridge, is_try_update_python_bridge
        )
