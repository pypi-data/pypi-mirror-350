import logging
from typing import Callable

from arpakitlib.ar_base_worker_util import safe_run_worker_in_background, SafeRunInBackgroundModes
from project.core.cache_file_storage_in_dir import get_cached_cache_file_storage_in_dir
from project.core.dump_file_storage_in_dir import get_cached_dump_file_storage_in_dir
from project.core.media_file_storage_in_dir import get_cached_media_file_storage_in_dir
from project.core.settings import get_cached_settings
from project.json_db.json_db import get_cached_json_db
from project.operation_execution.operation_executor_worker import create_operation_executor_worker
from project.operation_execution.scheduled_operation_creator_worker import create_scheduled_operation_creator_worker
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db

_logger = logging.getLogger(__name__)


# API STARTUP EVENTS


async def async_startup_api_event():
    _logger.info("start")

    if get_cached_media_file_storage_in_dir() is not None:
        get_cached_media_file_storage_in_dir().init()

    if get_cached_cache_file_storage_in_dir() is not None:
        get_cached_cache_file_storage_in_dir().init()

    if get_cached_dump_file_storage_in_dir() is not None:
        get_cached_dump_file_storage_in_dir().init()

    if (
            get_cached_sqlalchemy_db() is not None
            and get_cached_settings().api_init_sqlalchemy_db
    ):
        get_cached_sqlalchemy_db().init()

    if (
            get_cached_json_db() is not None
            and get_cached_settings().api_init_json_db
    ):
        get_cached_json_db().init()

    if get_cached_settings().api_start_operation_executor_worker:
        _ = safe_run_worker_in_background(
            worker=create_operation_executor_worker(),
            mode=SafeRunInBackgroundModes.thread
        )

    if get_cached_settings().api_start_scheduled_operation_creator_worker:
        _ = safe_run_worker_in_background(
            worker=create_scheduled_operation_creator_worker(),
            mode=SafeRunInBackgroundModes.async_task
        )

    _logger.info("finish")


def get_startup_api_events() -> list[Callable]:
    res = [async_startup_api_event]
    return res


# API SHUTDOWN EVENTS


async def async_shutdown_api_event():
    _logger.info("start")
    _logger.info("finish")


def get_shutdown_api_events() -> list[Callable]:
    res = [async_shutdown_api_event]
    return res
