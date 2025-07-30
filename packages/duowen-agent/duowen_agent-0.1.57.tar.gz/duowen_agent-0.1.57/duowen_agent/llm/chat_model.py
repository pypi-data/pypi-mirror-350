import os
from typing import List

from duowen_agent.error import LLMError, LengthLimitExceededError, MaxTokenExceededError
from duowen_agent.llm.entity import (
    MessagesSet,
    Message,
    openai_params_list,
)
from duowen_agent.llm.utils import format_messages
from duowen_agent.utils.core_utils import record_time, async_record_time
from openai import OpenAI, AsyncOpenAI


class OpenAIChat:
    def __init__(
        self,
        base_url: str = None,
        model: str = None,
        api_key: str = None,
        temperature: float = 0.2,
        top_p: float = None,
        presence_penalty: float = None,
        frequency_penalty: float = None,
        timeout: int = 120,
        token_limit: int = 4 * 1024,
        is_reasoning: bool = False,
        extra_headers: dict = None,
        extra_body: dict = None,
        **kwargs,
    ):
        """
        temperature 控制生成文本的随机性（值越低，输出越确定）。
        top_p 通过概率阈值控制输出的多样性（与 temperature 二选一）。
        presence_penalty 对已出现的内容进行惩罚（避免重复话题）。
        frequency_penalty 对高频内容进行惩罚（避免重复用词）。

        精确模式： 0.1, 0.3, 0.4, 0.7
        平衡模式： 0.5, 0.5, 0.4, 0.7
        自由模式： 0.9, 0.9, 0.4, 0.2
        """
        self.base_url = base_url or os.environ.get("OPENAI_BASE_URL", None)
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "xxx")
        self.temperature = temperature
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.model = model or kwargs.get("model_name", None) or "gpt-3.5-turbo"
        self.timeout = timeout
        self.token_limit = token_limit
        self.is_reasoning = is_reasoning
        self.extra_headers = extra_headers
        self.extra_body = extra_body
        self.kwargs = kwargs
        # qwen3 开启推理模式
        if self.is_reasoning and not self.extra_body and "qwen3" in self.model.lower():
            self.extra_body = {"enable_thinking": True}

    @property
    def sync_client(self) -> OpenAI:
        return OpenAI(
            api_key=self.api_key, base_url=self.base_url, timeout=self.timeout
        )

    @property
    def async_client(self) -> AsyncOpenAI:  # 新增异步客户端属性
        return AsyncOpenAI(
            api_key=self.api_key, base_url=self.base_url, timeout=self.timeout
        )

    def _check_message(
        self, message: str | List[dict] | List[Message] | MessagesSet
    ) -> MessagesSet:
        return format_messages(message, self.is_reasoning)

    def _build_params(
        self,
        messages: str | List[dict] | List[Message] | MessagesSet,
        temperature: float = None,
        top_p: float = None,
        presence_penalty: float = None,
        frequency_penalty: float = None,
        max_new_tokens: int = None,
        timeout: int = 30,
        forced_reasoning: bool = False,
        **kwargs,
    ):
        _message = self._check_message(messages)
        if self.is_reasoning:
            _message.remove_assistant_think()

        if self.is_reasoning and forced_reasoning and _message[-1].role == "user":
            _message.add_assistant("<think>\n")

        _params = {"messages": _message.get_messages(), "model": self.model}

        if temperature:
            _params["temperature"] = temperature
        elif self.temperature:
            _params["temperature"] = self.temperature

        if top_p:
            _params["top_p"] = top_p
        elif self.top_p:
            _params["top_p"] = self.top_p

        if presence_penalty:
            _params["presence_penalty"] = presence_penalty
        elif self.presence_penalty:
            _params["presence_penalty"] = self.presence_penalty

        if frequency_penalty:
            _params["frequency_penalty"] = frequency_penalty
        elif self.frequency_penalty:
            _params["frequency_penalty"] = self.frequency_penalty

        if max_new_tokens:
            _params["max_tokens"] = max_new_tokens
        else:
            _params["max_tokens"] = 2000

        if timeout:
            _params["timeout"] = timeout
        elif self.timeout:
            _params["timeout"] = self.timeout

        if self.extra_headers:
            _params["extra_headers"] = self.extra_headers

        if self.extra_body:
            _params["extra_body"] = self.extra_body

        if self.kwargs:
            for k, v in self.kwargs.items():
                if k in openai_params_list:
                    _params[k] = v

        if kwargs:
            for k, v in kwargs.items():
                if k in openai_params_list:
                    _params[k] = v
        return _params

    @record_time()
    def chat_for_stream(
        self,
        messages: str | List[dict] | List[Message] | MessagesSet,
        temperature: float = None,
        top_p: float = None,
        presence_penalty: float = None,
        frequency_penalty: float = None,
        max_new_tokens: int = None,
        timeout: int = 30,
        forced_reasoning=False,
        **kwargs,
    ):

        _params = self._build_params(
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            max_new_tokens=max_new_tokens,
            timeout=timeout,
            forced_reasoning=forced_reasoning,
            **kwargs,
        )
        _params["stream"] = True

        try:

            response = self.sync_client.chat.completions.create(**_params)

            _full_message = ""
            _is_think_start = False
            _is_think_end = False

            for chunk in response:
                if chunk.choices:
                    if chunk.choices[0].finish_reason == "length":
                        raise LengthLimitExceededError(content=_full_message)
                    elif chunk.choices[0].finish_reason == "max_tokens":
                        raise MaxTokenExceededError(content=_full_message)

                    _content_msg = chunk.choices[0].delta.content or ""
                    _reasoning_content_msg = (
                        chunk.choices[0].delta.reasoning_content or ""
                        if hasattr(chunk.choices[0].delta, "reasoning_content")
                        else ""
                    )

                    if _reasoning_content_msg and _is_think_start is False:
                        _msg = f"<think>\n{_reasoning_content_msg}"
                        _is_think_start = True
                    elif (
                        _content_msg
                        and _is_think_start is True
                        and _is_think_end is False
                    ):
                        _msg = f"\n</think>\n\n{_content_msg}"
                        _is_think_end = True
                    elif _reasoning_content_msg and _is_think_end is False:
                        _msg = _reasoning_content_msg
                    else:
                        _msg = _content_msg

                    _full_message += _msg

                    if _msg:
                        yield _msg

            if not _full_message:  # 如果流式输出返回为空
                raise LLMError(
                    "语言模型流式输出无响应", self.base_url, self.model, messages
                )

        except Exception as e:
            raise LLMError(str(e), self.base_url, self.model, messages)

    @async_record_time()
    async def achat_for_stream(
        self,
        messages: str | List[dict] | List[Message] | MessagesSet,
        temperature: float = None,
        top_p: float = None,
        presence_penalty: float = None,
        frequency_penalty: float = None,
        max_new_tokens: int = None,
        timeout: int = 30,
        forced_reasoning=False,
        **kwargs,
    ):

        _params = self._build_params(
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            max_new_tokens=max_new_tokens,
            timeout=timeout,
            forced_reasoning=forced_reasoning,
            **kwargs,
        )
        _params["stream"] = True

        try:

            response = await self.async_client.chat.completions.create(**_params)

            _full_message = ""
            _is_think_start = False
            _is_think_end = False

            async for chunk in response:
                if chunk.choices:
                    if chunk.choices[0].finish_reason == "length":
                        raise LengthLimitExceededError(content=_full_message)
                    elif chunk.choices[0].finish_reason == "max_tokens":
                        raise MaxTokenExceededError(content=_full_message)

                    _content_msg = chunk.choices[0].delta.content or ""
                    _reasoning_content_msg = (
                        chunk.choices[0].delta.reasoning_content or ""
                        if hasattr(chunk.choices[0].delta, "reasoning_content")
                        else ""
                    )

                    if _reasoning_content_msg and _is_think_start is False:
                        _msg = f"<think>\n{_reasoning_content_msg}"
                        _is_think_start = True
                    elif (
                        _content_msg
                        and _is_think_start is True
                        and _is_think_end is False
                    ):
                        _msg = f"\n</think>\n\n{_content_msg}"
                        _is_think_end = True
                    elif _reasoning_content_msg and _is_think_end is False:
                        _msg = _reasoning_content_msg
                    else:
                        _msg = _content_msg

                    _full_message += _msg

                    if _msg:
                        yield _msg

            if not _full_message:  # 如果流式输出返回为空
                raise LLMError(
                    "语言模型流式输出无响应", self.base_url, self.model, messages
                )

        except Exception as e:
            raise LLMError(str(e), self.base_url, self.model, messages)

    @record_time()
    def chat(
        self,
        messages: str | List[dict] | List[Message] | MessagesSet,
        temperature: float = None,
        top_p: float = None,
        presence_penalty: float = None,
        frequency_penalty: float = None,
        max_new_tokens: int = None,
        timeout: int = 30,
        forced_reasoning: bool = False,
        **kwargs,
    ):

        _params = self._build_params(
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            max_new_tokens=max_new_tokens,
            timeout=timeout,
            forced_reasoning=forced_reasoning,
            **kwargs,
        )
        _params["stream"] = False

        try:
            response = self.sync_client.chat.completions.create(**_params)

            if response.choices[0].finish_reason == "length":
                raise LengthLimitExceededError(
                    content=response.choices[0].message.content
                )
            elif response.choices[0].finish_reason == "max_tokens":
                raise MaxTokenExceededError(content=response.choices[0].message.content)
            else:
                _reasoning_content_msg = (
                    response.choices[0].message.reasoning_content
                    if hasattr(response.choices[0].message, "reasoning_content")
                    else ""
                )
                _content_msg = response.choices[0].message.content

                if _content_msg:
                    if _reasoning_content_msg:
                        return f"<think>\n{_reasoning_content_msg}</think>\n\n{_content_msg}"
                    return _content_msg
                else:
                    raise LLMError(
                        "语言模型无消息回复", self.base_url, self.model, messages
                    )

        except Exception as e:
            raise LLMError(str(e), self.base_url, self.model, messages)

    @async_record_time()
    async def achat(
        self,
        messages,
        temperature: float = None,
        top_p: float = None,
        presence_penalty: float = None,
        frequency_penalty: float = None,
        max_new_tokens: int = None,
        timeout: int = 30,
        forced_reasoning: bool = False,
        **kwargs,
    ):

        _params = self._build_params(
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            max_new_tokens=max_new_tokens,
            timeout=timeout,
            forced_reasoning=forced_reasoning,
            **kwargs,
        )
        _params["stream"] = False

        try:
            response = await self.async_client.chat.completions.create(**_params)

            if response.choices[0].finish_reason == "length":
                raise LengthLimitExceededError(
                    content=response.choices[0].message.content
                )
            elif response.choices[0].finish_reason == "max_tokens":
                raise MaxTokenExceededError(content=response.choices[0].message.content)
            else:
                _reasoning_content_msg = (
                    response.choices[0].message.reasoning_content
                    if hasattr(response.choices[0].message, "reasoning_content")
                    else ""
                )
                _content_msg = response.choices[0].message.content

                if _content_msg:
                    if _reasoning_content_msg:
                        return f"<think>\n{_reasoning_content_msg}</think>\n\n{_content_msg}"
                    return _content_msg
                else:
                    raise LLMError(
                        "语言模型无消息回复", self.base_url, self.model, messages
                    )

        except Exception as e:
            raise LLMError(str(e), self.base_url, self.model, messages)
