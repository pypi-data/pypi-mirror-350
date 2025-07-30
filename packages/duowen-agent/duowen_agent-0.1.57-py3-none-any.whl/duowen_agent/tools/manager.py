import json
from typing import List, Optional, Union, Any

from duowen_agent.tools.base import Tool


class ToolManager:
    """ToolManager helps Agent to manage tools"""

    def __init__(self, tools: List[Tool], filter_function_list: List[str] = None):
        self.tools: List[Tool] = tools
        self.filter_function_list = filter_function_list

    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Find specified tool by tool name.
        Args:
            tool_name(str): The name of the tool.

        Returns:
            Optional[Tool]: The specified tool or None if not found.
        """
        return next((tool for tool in self.tools if tool.name == tool_name), None)

    def run_tool(
        self, tool_name: str, parameters: Union[str, dict]
    ) -> tuple[str, Any | None]:
        """Run tool by input tool name and data inputs

        Args:
            tool_name(str): The name of the tool.
            parameters(Union[str, dict]): The parameters for the tool.

        Returns:
            str: The result of the tool.
            Any: 结构化数据用于页面展示
        """
        tool = self.get_tool(tool_name)

        if tool is None:
            return (
                f"{tool_name} has not been provided yet, please use the provided tool.",
                None,
            )

        if isinstance(parameters, dict):
            data = tool.run(**parameters)
        else:
            data = tool.run(parameters)

        if len(data) == 2:
            return data
        else:
            return data, None

    @property
    def tool_names(self) -> str:
        """Get all tool names."""
        tool_names = ""
        for tool in self.tools:
            tool_names += f"{tool.name}, "
        return tool_names[:-2]

    @property
    def tool_descriptions(self) -> str:
        """Get all tool descriptions, including the schema if available."""
        tool_descriptions = ""
        if self.filter_function_list:
            for tool in self.tools:
                if tool.name in self.filter_function_list:
                    tool_descriptions += (
                        json.dumps(
                            tool.to_schema(),
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
        else:
            for tool in self.tools:
                tool_descriptions += (
                    json.dumps(
                        tool.to_schema(),
                        ensure_ascii=False,
                    )
                    + "\n"
                )
        return tool_descriptions
