import logging
import time
from typing import Union, Optional, List, TypeVar

from duowen_agent.llm import OpenAIChat
from duowen_agent.tools.base import Tool
from duowen_agent.tools.manager import ToolManager
from duowen_agent.tools.mcp_client import McpClient
from duowen_agent.utils.string_template import StringTemplate
from pydantic import BaseModel

from .base import BaseAgent
from ..error import ObserverException
from ..prompt.prompt_build import prompt_now_day
from ..utils.core_utils import generate_unique_id, json_observation

REACT_SYSTEM_PROMPT_TEMPLATE = StringTemplate(
    template_format="jinja2",
    template="""
作为勤勉的任务代理，你的目标是尽可能高效地完成提供的任务或问题。

## Tools
你可以使用以下工具，工具信息通过以下结构描述提供：
{{tool_descriptions}}

## Output Format
请使用以下JSON格式回答问题。仅返回JSON，不要有解释。否则将会受到惩罚。
输出必须符合以下JSON格式规范。仅返回JSON，不要解释。

```json
{
"analysis": "当前操作思路及原因分析",
"action": # 要采取的动作，必须是提供的工具之一
    {
    "name": "工具名称",
    "args": "工具输入参数，JSON格式数据"
    }
}
```

如果使用此格式，用户将按以下格式回应：

```
Observation: tool response
```

你应持续重复上述格式，直到获得足够信息无需继续使用工具即可回答问题。此时必须改用以下两种格式之一：

- 若能回答问题：

```json
{
"analysis": "最终判断依据及结论",
"action": {
    "name": "finish",
    "args": {"content": "你的答案"}
    }
}
```

- 若当前上下文无法回答问题：

```json
{
"analysis": "无法解决的原因分析",
"action": {
    "name": "finish",
    "args": {"content": "抱歉，我无法回答您的查询，因为（总结所有步骤并说明原因）"}
    }
}
```

## Attention
- 仅返回JSON格式，不要有解释
- 每一步只能选择一个工具
- 最终答案语言需与用户提问语言一致
- 动作参数的格式（JSON或字符串）取决于工具定义

## User question
{{question}}

## Current Conversation
以下是当前对话历史记录，包含交替的用户提问和助手回复：

""",  # noqa: E501
)
PREFIX_TEMPLATE = """你是一个{agent_identity}，名为{agent_name}，你的目标是{agent_goal}，限制条件是{agent_constraints}。"""  # noqa


REACT_SYSTEM_PROMPT_EN_TEMPLATE = StringTemplate(
    template_format="jinja2",
    template="""
As a diligent Task Agent, you goal is to effectively accomplish the provided task or question as best as you can.

## Tools
You have access to the following tools, the tools information is provided by the following schema:
{{tool_descriptions}}

## Output Format
To answer the question, Use the following JSON format. JSON only, no explanation. Otherwise, you will be punished.
The output should be formatted as a JSON instance that conforms to the format below. JSON only, no explanation.

```json
{
"analysis": "The thought of what to do and why.",
"action": # the action to take, must be one of provided tools
    {
    "name": "tool name",
    "args": "tool input parameters, json type data"
    }
}
```

If this format is used, the user will respond in the following format:

```
Observation: tool response
```

You should keep repeating the above format until you have enough information
to answer the question without using any more tools. At that point, you MUST respond
in the one of the following two formats:

- If you can answer the question:

```json
{
"analysis": "The thought of what to do and why.",
"action": {
    "name": "finish",
    "args": {"content": "You answer here."}
    }
}
```

- If you cannot answer the question in the current context:

```json
{
"analysis": "The thought of what to do and why.",
"action": {
    "name": "finish",
    "args": {"content": "Sorry, I cannot answer your query, because (Summary all the upper steps, and explain)"}
    }
}
```

## Attention
- Your output is JSON only and no explanation.
- Choose only ONE tool and you can't do without using any tools in one step.
- Your final answer output language should be consistent with the language used by the user. Middle step output is English.
- Whether the action input is JSON or str depends on the definition of the tool.

## User question
{{question}}

## Current Conversation
Below is the current conversation consisting of interleaving human and assistant history.

""",  # noqa: E501
)
PREFIX_EN_TEMPLATE = """You are a {agent_identity}, named {agent_name}, your goal is {agent_goal}, and the constraint is {agent_constraints}. """  # noqa


class ActionResponseArgs(BaseModel):
    name: str
    args: Union[dict, str]


class ActionResponse(BaseModel):
    analysis: str
    action: ActionResponseArgs


class ReactThink(BaseModel):
    content: str
    cell_id: str


class ReactActionParameters(BaseModel):
    analysis: Optional[str] = None
    action_name: str
    action_parameters: Optional[dict] = None


class ReactAction(BaseModel):
    action: ReactActionParameters
    cell_id: str


T = TypeVar("T")


class ReactObservationResult(BaseModel):
    result: str
    view: Optional[T] = None


class ReactObservation(BaseModel):
    observation: ReactObservationResult
    action: ReactActionParameters
    exec_status: bool
    cell_id: str


class ReactResult(BaseModel):
    result: str
    cell_id: str


class ReactAgent(BaseAgent):

    def __init__(
        self,
        *,
        llm: OpenAIChat,
        tools: List[Tool] = None,
        mcp_client: Optional[McpClient] = None,
        prefix_prompt_template: StringTemplate = StringTemplate(PREFIX_TEMPLATE),
        filter_function_list: List[str] = None,
        enable_role: bool = False,
        agent_name: str = "tool-agent",
        agent_identity: str = "tool-agent",
        agent_goal: str = "provides better assistance and services for humans.",
        agent_constraints: str = "none",
        max_iterations: Optional[int] = 15,
        _from: Optional[str] = None,
        **kwargs,
    ):
        super().__init__()
        self.tool_manager = ToolManager(tools, filter_function_list) if tools else None
        self.mcp_client = mcp_client
        self.llm = llm
        self.system_prompt_template: StringTemplate = REACT_SYSTEM_PROMPT_TEMPLATE
        self.prefix_prompt_template: StringTemplate = prefix_prompt_template
        self.conversation_prompt: str = ""
        self.filter_function_list = filter_function_list
        self.max_iterations = max_iterations
        self.max_execution_time: Optional[float] = None

        self.enable_role: bool = enable_role
        self.agent_name: str = agent_name
        self.agent_identity: str = agent_identity
        self.agent_goal: str = agent_goal
        self.agent_constraints: str = agent_constraints

    def get_llm(self) -> OpenAIChat:
        return self.llm

    def _build_system_prompt(self, instruction: str) -> str:
        prefix_prompt = (
            self.prefix_prompt_template.format(
                agent_identity=self.agent_identity,
                agent_name=self.agent_name,
                agent_goal=self.agent_goal,
                agent_constraints=self.agent_constraints,
            )
            if self.enable_role
            else ""
        )

        _func_tool_descriptions = (
            self.tool_manager.tool_descriptions if self.tool_manager else "\n"
        )

        _mpc_tool_descriptions = (
            self.mcp_client.tool_descriptions if self.mcp_client else "\n"
        )

        return prefix_prompt + self.system_prompt_template.format(
            question=instruction,
            tool_descriptions=_func_tool_descriptions + _mpc_tool_descriptions,
        )

    @property
    def current_date(self) -> str:
        return prompt_now_day()
        # f"Current date: {time.strftime('%Y-%m-%d %H:%M:%S')}"

    def _run(
        self, instruction: str, return_raw_data: bool = False, **kwargs
    ) -> Union[str, ActionResponse]:
        self.conversation_prompt = self._build_system_prompt(instruction)
        logging.debug(f"[agent] ToolAgent system prompt: {self.conversation_prompt}")

        iterations = 0
        used_time = 0.0
        start_time = time.time()

        while self._should_continue(iterations, used_time):
            llm_resp: str = ""

            cell_id = generate_unique_id("react")
            for i in self.llm.chat_for_stream(
                messages=self.conversation_prompt + self.current_date
            ):
                yield ReactThink(content=i, cell_id=cell_id)
                llm_resp += i

            while llm_resp == "":
                llm_resp: str = ""

                for i in self.llm.chat(
                    messages=self.conversation_prompt + self.current_date
                ):
                    yield ReactThink(content=i, cell_id=cell_id)
                    llm_resp += i

            try:
                action_resp: ActionResponse = self._parse_llm_response(llm_resp)
            except ObserverException as e:
                logging.warning(f"ReactAction parse llm response error: {str(e)}")
                continue

            yield ReactAction(
                **{
                    "action": {
                        "analysis": action_resp.analysis,
                        "action_name": action_resp.action.name,
                        "action_parameters": action_resp.action.args,
                    },
                    "cell_id": cell_id,
                }
            )

            self.conversation_prompt += f"\nAction:{llm_resp}\n"
            logging.debug(
                f"[dw] tool agent <{iterations}> current prompt: {self.conversation_prompt}"  # noqa
            )

            if "finish" in action_resp.action.name:
                if return_raw_data:
                    yield ReactResult(result=action_resp, cell_id=cell_id)

                yield ReactResult(
                    result=action_resp.action.args["content"], cell_id=cell_id
                )
                return

            try:
                tool_result, tool_result_meta = self.run_tool(
                    action_resp.action.name, action_resp.action.args
                )
                tool_exec_status = True
            except ObserverException as e:
                tool_result, tool_result_meta = str(e), None
                tool_exec_status = False
            except Exception as e:
                tool_result, tool_result_meta = str(e), None
                tool_exec_status = False

            self.conversation_prompt += f"Observation: {tool_result}\n"
            yield ReactObservation(
                **{
                    "observation": {"result": tool_result, "view": tool_result_meta},
                    "action": {
                        "analysis": action_resp.analysis,
                        "action_name": action_resp.action.name,
                        "action_parameters": action_resp.action.args,
                    },
                    "exec_status": tool_exec_status,
                    "cell_id": cell_id,
                }
            )
            iterations += 1
            used_time += time.time() - start_time

    def run_tool(self, tool_name: str, parameters: Union[str, dict]):

        if self.tool_manager and self.tool_manager.get_tool(tool_name):
            return self.tool_manager.run_tool(tool_name, parameters)
        elif self.mcp_client.get_tool_info(tool_name):
            return self.mcp_client.run_tool(tool_name, parameters), None
        else:
            return f"未知的工具调用{tool_name}", None

    def _should_continue(self, current_iteration: int, current_time_elapsed) -> bool:
        if self.max_iterations and current_iteration >= self.max_iterations:
            return False
        if self.max_execution_time and current_time_elapsed >= self.max_execution_time:
            return False
        return True

    @staticmethod
    def _parse_llm_response(llm_resp: str) -> ActionResponse:
        return json_observation(llm_resp, ActionResponse)
