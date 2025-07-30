from typing import List

from .entity import Message, MessagesSet, UserMessage, SystemMessage


def format_messages(
    message: str | List[dict] | List[Message] | MessagesSet, is_reasoning=False
) -> MessagesSet:
    if isinstance(message, str):
        if is_reasoning:
            return MessagesSet(
                message_list=[
                    UserMessage(message),
                ]
            )
        else:
            return MessagesSet(
                [
                    SystemMessage("You are a helpful assistant"),
                    UserMessage(message),
                ]
            )
    elif type(message) is MessagesSet:
        return message
    elif isinstance(message, List) and all(isinstance(i, Message) for i in message):
        return MessagesSet(message)
    elif isinstance(message, List) and all(isinstance(i, dict) for i in message):
        return MessagesSet().init_message_list(message)
    else:
        raise ValueError(f"message 格式非法:{str(message)}")
