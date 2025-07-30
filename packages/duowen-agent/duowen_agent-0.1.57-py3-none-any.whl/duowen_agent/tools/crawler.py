from typing import Literal

import requests
from duowen_agent.rag.extractor.simple import html2md
from pydantic import BaseModel, Field

from .base import Tool


class CrawlerParams(BaseModel):
    url: str = Field(description="the url need to crawl")
    return_type: Literal["html", "text"] = Field(
        default="text", description="the return type of the crawler, html or text"
    )


class Crawler(Tool):

    name: str = "crawler"
    description: str = "A tool to crawl the web and return the content of the url"
    parameters = CrawlerParams

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, url, return_type="text") -> str:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                if return_type == "html":
                    return response.text
                elif return_type == "text":
                    return html2md(response.text)
        except Exception as e:
            return "无法获取网页内容"
