import json
import re
from typing import Callable, Optional, Literal, Union

from duowen_agent.agents.component.base import BaseComponent
from duowen_agent.error import ObserverException
from duowen_agent.llm import OpenAIChat, MessagesSet
from duowen_agent.prompt.prompt_build import prompt_now_day
from duowen_agent.tools.entity import ToolSearchResult
from duowen_agent.utils.core_utils import (
    json_observation,
    generate_unique_id,
    remove_think,
)
from duowen_agent.utils.string_template import StringTemplate
from pydantic import BaseModel, Field


def extract_between(text: str, start_tag: str, end_tag: str) -> list[str]:
    pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
    return re.findall(pattern, text, flags=re.DOTALL)


class DeepSearchThink(BaseModel):
    content: str
    cell_id: str


class DeepSearchAction(BaseModel):
    content: str
    cell_id: str


class DeepSearchObservation(BaseModel):
    result: str
    view: Optional[Union[ToolSearchResult, str]] = None
    ask_type: Literal["llm", "retrieval", "preset", "finish"] = Field(
        "retrieval",
        description="llm:模型回答 retrieval:检索回答 preset:系统预设回答 finish:结束",
    )
    search_query: Optional[str] = None
    cell_id: str


class DeepSearchQA(BaseComponent):

    def __init__(self, llm_instance: OpenAIChat, **kwargs):
        self.llm_instance = llm_instance
        self.kwargs = kwargs

    @staticmethod
    def build_prompt() -> StringTemplate:
        return StringTemplate(
            """**任务说明**

你需基于以下输入内容进行分析：**历史推理步骤**，**当前搜索词**和**已检索网页**。你的目标是从**已检索网页**中提取与**当前搜索词**相关的有效信息，并将这些信息无缝整合到**历史推理步骤**中以继续回答原始问题。

**操作指南**

1. **分析网页内容**
- 仔细阅读每个网页的内容
- 识别与当前搜索词相关的事实性信息

2. **提取相关信息**
- 选择能推进推理进程的关键信息
- 确保信息准确且相关

3. **输出格式**
- **若存在有效信息**：以下列格式开头呈现
- 搜索语言必须与'搜索词'或'网页内容'保持相同\n"

**最终信息**

[有效信息]

- **若无有效信息**：输出以下内容

**最终信息**

未找到有效信息

**输入内容**
- **历史推理步骤**  
{prev_reasoning}

- **当前搜索词**  
{search_query}

- **已检索网页**  
{document}

"""
        )

    async def arun(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, search_query, prev_reasoning, document) -> str:

        _prompt = (
            MessagesSet()
            .add_system(
                self.build_prompt().format(
                    prev_reasoning=prev_reasoning,
                    search_query=search_query,
                    document=document,
                )
            )
            .add_user(
                f'请基于当前搜索词"{search_query}"并结合已有推理步骤，逐一分析网页内容并提取有效信息。'
            )
        )

        # print(_prompt.get_format_messages())
        # print(
        #     "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        # )

        return self.llm_instance.chat(_prompt)


def _get_prompt(
    max_search_limit: int = 15,
) -> MessagesSet:
    _prompt = MessagesSet()

    _prompt.add_system(
        StringTemplate(
            """
---
CURRENT_TIME: {{ current_time  }}
---
            
你是一个具备数据集搜索能力的推理助手，可以通过搜索数据集来准确回答用户问题。你拥有特殊工具：

- 执行搜索时：
输入 Question: 你的查询 
系统将搜索并分析相关内容，随后json格式返回有效信息
```json
{
  "analysis": "当前操作思路及原因分析",
  "action": {
    "name": "search",
    "args": "你的检索词"
  }
}
```

- 当已获取足够信息回答问题
系统将搜索并分析相关内容，随后json格式返回有效信息
```json
{
  "analysis": "最终判断依据及结论",
  "action": {
    "name": "finish",
    "args": "你的回答"
  }
}
```

如有需要可以多次重复搜索流程。最大搜索尝试次数限制为 {{max_search_limit}} 次

当获取到足够信息后，请继续你的推理过程


**重要提示**：
- 你拥有数据集搜索能力，只需提供合适的搜索词
- 搜索语言必须与'问题'或'搜索结果'保持相同
- 若无有效信息，请精简搜索词并确保关键词精确
- 完成搜索后请继续推理过程
请回答以下问题，你需要通过逐步推理来解决问题
""",
            template_format="jinja2",
        ).format(max_search_limit=max_search_limit, current_time=prompt_now_day())
    )

    _prompt.add_user(
        "Question:《大白鲨》和《007：大战皇家赌场》的导演是否来自同一个国家？"
    )

    _prompt.add_assistant(
        """```json
{
  "analysis": "为了回答这个问题，我需要分别查找《大白鲨》和《007：大战皇家赌场》的导演信息。首先，我将查找《大白鲨》的导演是谁。",
  "action": {
    "name": "search",
    "args": "《大白鲨》的导演是谁？"
  }
}
```"""
    )

    _prompt.add_user("Observation:《大白鲨》的导演是史蒂文·斯皮尔伯格")

    _prompt.add_assistant(
        """```json
{
  "analysis": "根据搜索结果，《大白鲨》的导演是史蒂文·斯皮尔伯格。接下来，我们需要查找史蒂文·斯皮尔伯格来自哪里？",
  "action": {
    "name": "search",
    "args": "史蒂文·斯皮尔伯格来自哪里？"
  }
}
```"""
    )

    _prompt.add_user("Observation: 史蒂文·艾伦·斯皮尔伯格是美国电影导演")

    _prompt.add_assistant(
        """```json
{
  "analysis": "根据搜索结果，《大白鲨》的导演是史蒂文·斯皮尔伯格，他是美国人。接下来，我们需要查找《007：大战皇家赌场》的导演信息。",
  "action": {
    "name": "search",
    "args": "《007：大战皇家赌场》的导演是谁？"
  }
}
```"""
    )
    _prompt.add_user("Observation: 该片由马丁·坎贝尔执导")

    _prompt.add_assistant(
        """```json
{
  "analysis": "根据搜索结果，《007：大战皇家赌场》的导演是马丁·坎贝尔。接下来，我们需要查找马丁·坎贝尔来自哪里？",
  "action": {
    "name": "search",
    "args": "马丁·坎贝尔来自哪里？"
  }
}
```"""
    )

    _prompt.add_user("Observation: 马丁·坎贝尔（1943年10月24日出生）是新西兰导演")

    _prompt.add_assistant(
        """```json
{
  "analysis": "根据搜索结果，史蒂文·斯皮尔伯格是美国人，而马丁·坎贝尔是新西兰人。因此，他们来自不同的国家。",
  "action": {
    "name": "finish",
    "args": "《大白鲨》和《007：大战皇家赌场》的导演不来自同一个国家。"
  }
}
```"""
    )

    _prompt.add_user("Question: Craigslist创始人何时出生？")

    _prompt.add_assistant(
        """```json
{
  "analysis": "为了回答这个问题，我需要首先查找Craigslist的创始人是谁。然后，我将查找该创始人的出生日期。首先，我将查找Craigslist的创始人信息。",
  "action": {
    "name": "search",
    "args": "Craigslist的创始人是谁？"
  }
}
```"""
    )

    _prompt.add_user("Observation: Craigslist由克雷格·纽马克创立")

    _prompt.add_assistant(
        """```json
{
  "analysis": "根据搜索结果，Craigslist由克雷格·纽马克创立。接下来，我将查找克雷格·纽马克的出生日期。",
  "action": {
    "name": "search",
    "args": "克雷格·纽马克的出生日期？"
  }
}
```"""
    )
    _prompt.add_user("Observation: 克雷格·纽马克出生于1952年12月6日")

    _prompt.add_assistant(
        """```json
{
  "analysis": "根据搜索结果，Craigslist的创始人克雷格·纽马克出生于1952年12月6日。",
  "action": {
    "name": "finish",
    "args": "Craigslist的创始人克雷格·纽马克出生于1952年12月6日。"
  }
}
```"""
    )
    return _prompt


class InferenceAction(BaseModel):
    name: Literal["search", "finish"]
    args: str


class Inference(BaseModel):
    analysis: str
    action: InferenceAction


class DeepSearch:
    def __init__(
        self,
        llm_plann_instance: OpenAIChat,
        retrieval: Callable[[str], ToolSearchResult],
        max_search_limit: int = 15,
        llm_answer_instance: OpenAIChat = None,
        self_qa_llm_instance: OpenAIChat = None,
    ):
        self.llm_plann_instance = llm_plann_instance
        self.llm_answer_instance = llm_answer_instance or llm_plann_instance
        self.retrieval = retrieval
        self.max_search_limit = max_search_limit
        self.self_qa_llm_instance = self_qa_llm_instance

    def run(self, question: str):

        _prompt = _get_prompt(max_search_limit=self.max_search_limit + 6)

        executed_search_queries = []
        all_reasoning_steps = []

        for ii in range(self.max_search_limit + 1):
            cell_id = generate_unique_id("deepsearch")
            if ii == 0:
                _prompt.add_user(f"""Question: {prompt_now_day()}, {question}""")
                all_reasoning_steps.append(
                    f"""Question:  {prompt_now_day()}, {question}"""
                )

            elif ii == self.max_search_limit - 1:
                summary_think = "当前操作已触发搜索次数上限，系统禁止继续执行搜索请求。"
                yield DeepSearchObservation(
                    result=summary_think,
                    ask_type="preset",
                    cell_id=cell_id,
                )
                all_reasoning_steps.append(f"Observation: {summary_think}")
                _prompt.add_user(f"Observation: {summary_think}")

                # print(_prompt.get_format_messages())
                # print(
                #     "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                # )

                _res = self.llm_plann_instance.chat(_prompt)
                try:
                    _res = json_observation(_res, Inference)
                    yield DeepSearchAction(
                        content=_res.analysis,
                        cell_id=cell_id,
                    )
                    yield DeepSearchObservation(
                        result=_res.action.args,
                        ask_type="finish",
                        cell_id=cell_id,
                    )
                except ObserverException as e:
                    yield DeepSearchObservation(
                        result=str(e),
                        ask_type="finish",
                        cell_id=cell_id,
                    )
                break  # 退出循环

            if _prompt.get_last_message().role != "user":
                _prompt.add_user(f"Observation: 基于新信息持续执行推理链路。")

            # print(_prompt.get_format_messages())
            # print(
            #     "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            # )

            res = self.llm_plann_instance.chat(_prompt)

            # print(res)
            # print(
            #     "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            # )

            try:
                ans: Inference = json_observation(res, Inference)
            except ObserverException as e:
                all_reasoning_steps.append(f"Observation: {str(e)}")
                _prompt.add_assistant(res)
                _prompt.add_user(f"Observation: {str(e)}")
                continue

            _assistant_content = f"```json\n{json.dumps(ans.model_dump(), indent=2,ensure_ascii=False)}\n```"
            _prompt.add_assistant(_assistant_content)
            all_reasoning_steps.append(f"""Action:\n{_assistant_content}""")

            yield DeepSearchThink(
                content=ans.analysis,
                cell_id=cell_id,
            )

            if ans.action.name == "finish":
                yield DeepSearchObservation(
                    result=ans.action.args,
                    ask_type="finish",
                    cell_id=cell_id,
                )
                break  # 退出循环

            elif (
                ans.action.name == "search"
                and ans.action.args in executed_search_queries
            ):
                yield DeepSearchAction(
                    content=ans.action.args,
                    cell_id=cell_id,
                )

                yield DeepSearchObservation(
                    result="检测到重复查询请求，直接调用历史搜索结果。",
                    ask_type="preset",
                    cell_id=cell_id,
                    search_query=ans.action.args,
                )
                all_reasoning_steps.append(
                    f"Observation: 检测到重复查询请求，直接调用历史搜索结果。"
                )
                _prompt.add_user(
                    f"Observation: 检测到重复查询请求，直接调用历史搜索结果。"
                )
                continue

            elif ans.action.name == "search":

                yield DeepSearchAction(
                    content=ans.action.args,
                    cell_id=cell_id,
                )

                _doc = self.retrieval(ans.action.args)

                if not _doc.result:
                    if self.self_qa_llm_instance:
                        res = self.self_qa_llm_instance.chat(
                            MessagesSet()
                            .add_system(
                                "请用中立、客观的方式回答以下问题，语言需简明扼要（不超过3-5句话），避免主观推测或冗长解释。如果问题涉及争议性话题，请提供事实性信息并平衡相关观点。",
                            )
                            .add_user(f"问题: {ans.action.args}")
                        )
                        res = remove_think(res)

                        yield DeepSearchObservation(
                            result=res,
                            ask_type="llm",
                            cell_id=cell_id,
                            search_query=ans.action.args,
                        )
                        all_reasoning_steps.append(f"Observation: {res}")
                        _prompt.add_user(f"Observation: {res}")
                    else:

                        yield DeepSearchObservation(
                            result="未检索到有效信息",
                            ask_type="preset",
                            cell_id=cell_id,
                            search_query=ans.action.args,
                        )
                        all_reasoning_steps.append(f"Observation: 未检索到有效信息")
                        _prompt.add_user(f"Observation: 未检索到有效信息")
                else:
                    res = DeepSearchQA(self.llm_answer_instance).run(
                        search_query=ans.action.args,
                        prev_reasoning="\n\n".join(all_reasoning_steps),
                        document=_doc.content_with_weight,
                    )
                    res = remove_think(res)
                    yield DeepSearchObservation(
                        result=res,
                        view=_doc,
                        ask_type="retrieval",
                        cell_id=cell_id,
                        search_query=ans.action.args,
                    )
                    all_reasoning_steps.append(f"Observation: {res}")
                    _prompt.add_user(f"Observation: {res}")
