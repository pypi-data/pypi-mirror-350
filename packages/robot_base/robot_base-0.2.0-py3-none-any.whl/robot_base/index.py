import time
from functools import wraps

from .log_util import Logger


def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "code_block_extra_data" in kwargs:
            extra_data = kwargs["code_block_extra_data"]
            code_line_number = extra_data.get("code_line_number", "")
            code_file_name = extra_data.get("code_file_name", "")
            code_block_name = extra_data.get("code_block_name", "")
            Logger.get_logger().debug(
                "正在执行:" + code_block_name + "," + str(args) + "," + str(kwargs)
            )
            Logger.get_logger().info(
                f"正在执行:[{code_file_name}] 的第 [{code_line_number}] 行的 [{code_block_name}]"
            )
            return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


def func_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "code_block_extra_data" in kwargs:
            extra_data = kwargs["code_block_extra_data"]
            exception_data = extra_data.get("exception", {})
            retry_count = int(exception_data.get("retry_count", 0))
            delayed_execution_time = exception_data.get("delayed_execution_time", 0)
            retry_interval = float(exception_data.get("retry_interval", 0))
            ignore_exception = exception_data.get("exception", "error") == "continue"
            code_map_id = extra_data.get("code_map_id", "")
            code_block_name = extra_data.get("code_block_name", "")
            if delayed_execution_time > 0:
                time.sleep(delayed_execution_time)
            current_count = 0
            while current_count <= retry_count:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    current_count = current_count + 1
                    if retry_interval > 0:
                        time.sleep(retry_interval)
                    if current_count > retry_count and not ignore_exception:
                        raise Exception(
                            "code_map_id:" + code_map_id, code_block_name, e
                        )
        else:
            return func(*args, **kwargs)

    return wrapper


class ParamException(Exception):
    """
    参数异常，不可重试
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class TemporaryException(Exception):
    """
    临时异常，可重试
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
