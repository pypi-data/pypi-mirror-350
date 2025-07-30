import html

from pydantic import BaseModel, field_validator
from pydantic_core import Url
from typing_extensions import TypedDict


class SlackProfile(TypedDict):
    real_name: str
    real_name_normalized: str
    display_name: str
    display_name_normalized: str
    status_text: str
    status_emoji: str
    email: str
    image_24: str
    image_32: str
    image_48: str
    image_72: str
    image_192: str
    image_512: str
    is_bot: bool


class FormInput(BaseModel):
    token: str
    team_id: str
    team_domain: str
    channel: str
    channel_name: str
    user_id: str
    user_name: str
    command: str
    text: str = ""
    api_app_id: str
    is_enterprise_install: bool
    response_url: Url
    trigger_id: str

    @field_validator("command")
    def command_validate(cls, value: str):
        value = html.unescape(value)
        if value.startswith("/"):
            return value[1:]
        raise ValueError("A slash command must start with a '/' character.")
