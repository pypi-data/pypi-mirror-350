from dataclasses import field
from typing import Optional

from vajra.entrypoints.config import APIServerConfig
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class OpenAIServerConfig(APIServerConfig):
    api_key: Optional[str] = field(
        default=None, metadata={"help": "API key for authentication with the server."}
    )
    chat_template: Optional[str] = field(
        default=None, metadata={"help": "Template for formatting chat messages."}
    )
    response_role: str = field(
        default="assistant",
        metadata={
            "help": "Role to be assigned to the model's responses in the chat format."
        },
    )
