import asyncio
import logging
import random
import re
import string
import time
from functools import wraps
from importlib import import_module
from typing import Callable, Any
from typing import Coroutine, Dict, List, Optional, Type

import json5
from pydantic import ValidationError, BaseModel

from duowen_agent.error import ObserverException

logger = logging.getLogger(__name__)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.

    Args:
        dotted_path: eg promptulate.schema.MessageSet

    Returns:
        Class corresponding to dotted path.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class'
            % (module_path, class_name)
        ) from err


def listdict_to_string(
    data: List[Dict],
    prefix: Optional[str] = "",
    suffix: Optional[str] = "\n",
    item_prefix: Optional[str] = "",
    item_suffix: Optional[str] = ";\n\n",
    is_wrap: bool = True,
) -> str:
    """Convert List[Dict] type data to string type"""
    wrap_ch = "\n" if is_wrap else ""
    result = f"{prefix}"
    for item in data:
        temp_list = ["{}:{} {}".format(k, v, wrap_ch) for k, v in item.items()]
        result += f"{item_prefix}".join(temp_list) + f"{item_suffix}"
    result += suffix
    return result[:-2]


def generate_unique_id(prefix: str = "dw") -> str:
    timestamp = int(time.time() * 1000)
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=6))

    unique_id = f"{prefix}-{timestamp}-{random_string}"
    return unique_id


def convert_backslashes(path: str):
    """Convert all \\ to / of file path."""
    return path.replace("\\", "/")


def hint(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ret = fn(*args, **kwargs)
        logger.debug(f"function {fn.__name__} is running now")
        return ret

    return wrapper


def remove_think(content: str):
    pattern = r"<think>.*?</think>"
    cleaned_text = re.sub(pattern, "", content, count=1, flags=re.DOTALL)
    return cleaned_text.strip()


def extract_think(content: str):
    pattern = r"<think>(.*?)</think>"
    match = re.search(pattern, content, flags=re.DOTALL)
    return match.group(1).strip() if match else None


def separate_reasoning_and_response(content: str):
    return {
        "content": remove_think(content),
        "content_reasoning": extract_think(content),
    }


def record_time():
    def decorator(fn: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            start_time = time.time()
            ret = fn(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"[duowen-agent timer] <{fn.__name__}> run {duration}s")
            return ret

        return wrapper

    return decorator


def async_record_time():
    """异步函数设计的执行时间记录装饰器
    @async_record_time()
    async def async_operation():
        await asyncio.sleep(1.5)
        # 模拟异步操作
        return "result"
    """

    def decorator(fn: Callable[..., Coroutine]) -> Callable[..., Coroutine]:
        @wraps(fn)
        async def async_wrapper(*args, **kwargs) -> Coroutine:
            start_time = time.time()
            try:
                # 注意这里需要使用 await 来等待异步函数执行
                return await fn(*args, **kwargs)
            finally:
                # 使用高精度时间计算
                duration = time.time() - start_time
                logger.debug(
                    f"[duowen-agent async-timer] <{fn.__name__}> run {duration:.4f}s"
                )

        # # 类型检查确保装饰的是协程函数
        # if not asyncio.iscoroutinefunction(fn):
        #     raise TypeError(
        #         "async_record_time decorator can only be applied to async functions"
        #     )

        return async_wrapper

    return decorator


def retrying(_func, _max_retries=3, **kwargs):
    for attempt in range(_max_retries):
        try:
            return _func(**kwargs)
        except ObserverException:
            if attempt == _max_retries - 1:
                raise
            else:
                time.sleep(0.1)
                continue
        except Exception as e:
            raise


async def aretrying(_func: Callable[..., Any], _max_retries: int = 3, **kwargs) -> Any:
    """异步重试函数（支持协程函数的重试机制）"""
    for attempt in range(1, _max_retries + 1):
        try:
            # 异步等待函数执行，兼容协程返回值
            return await _func(**kwargs)
        except ObserverException:
            if attempt == _max_retries:
                raise  # 最后一次重试仍失败则抛出原异常
            await asyncio.sleep(0.1 * attempt)  # 指数退避策略
        except Exception as e:
            # 其他异常直接抛出，中断重试
            raise

    raise RuntimeError("Unexpected code path")


def parse_json_markdown(json_string: str) -> dict:
    # Get json from the backticks/braces
    json_string = json_string.strip()
    starts = ["```json", "```", "``", "`", "{"]
    ends = ["```", "``", "`", "}"]
    end_index = -1
    for s in starts:
        start_index = json_string.find(s)
        if start_index != -1:
            if json_string[start_index] != "{":
                start_index += len(s)
            break
    if start_index != -1:
        for e in ends:
            end_index = json_string.rfind(e, start_index)
            if end_index != -1:
                if json_string[end_index] == "}":
                    end_index += 1
                break
    if start_index != -1 and end_index != -1 and start_index < end_index:
        extracted_content = json_string[start_index:end_index].strip()
        parsed = json5.loads(extracted_content)
    else:
        logging.error(f"parse_json_markdown content: {json_string}")
        raise Exception("Could not find JSON block in the output.")

    return parsed


def json_observation(content: str, pydantic_obj: Type[BaseModel]):
    try:
        _content = remove_think(content)
        _data1 = parse_json_markdown(_content)
    except ValueError as e:
        raise ObserverException(
            predict_value=remove_think(content) if "<think>" in content else content,
            expect_value="json format data",
            err_msg=f"observation error jsonload, msg: {str(e)}",
        )
    try:
        return pydantic_obj(**_data1)
    except ValidationError as e:
        raise ObserverException(
            predict_value=_content,
            expect_value=str(pydantic_obj.model_json_schema()),
            err_msg=f"observation error ValidationError, msg: {str(e)}",
        )
