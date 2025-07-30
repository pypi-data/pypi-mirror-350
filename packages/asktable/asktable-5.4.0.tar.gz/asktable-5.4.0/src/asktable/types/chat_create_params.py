# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import TypedDict

__all__ = ["ChatCreateParams"]


class ChatCreateParams(TypedDict, total=False):
    bot_id: Optional[str]
    """
    机器人 ID，如果需要使用高级功能，请使用 bot_id 来创建对话。在机器人中你可以定义
    可以访问的数据、可以执行的任务以及是否开启调试模式等设置。
    """

    name: Optional[str]
    """New name for the chat"""

    role_id: Optional[str]
    """
    角色 ID，将扮演这个角色来执行对话，用于权限控制。若无，则跳过鉴权，即可查询所有
    数据
    """

    role_variables: Optional[Dict[str, Union[str, int, bool]]]
    """在扮演这个角色时需要传递的变量值，用 Key-Value 形式传递"""

    user_profile: Optional[Dict[str, Union[str, int, bool]]]
    """用户信息，用于在对话中传递用户的信息，用 Key-Value 形式传递"""
