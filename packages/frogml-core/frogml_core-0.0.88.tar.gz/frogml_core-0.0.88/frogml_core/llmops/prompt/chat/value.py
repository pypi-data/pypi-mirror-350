from dataclasses import dataclass
from typing import List

from frogml_core.llmops.prompt.chat.message import BaseMessage
from frogml_core.llmops.prompt.value import PromptValue


@dataclass
class ChatPromptValue(PromptValue):
    messages: List[BaseMessage]
