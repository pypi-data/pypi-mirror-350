import random

from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11.event import (
    GroupMessageEvent,
    MessageEvent,
    PrivateMessageEvent,
)

from .config import config_manager
from .utils import (
    get_current_datetime_timestamp,
    get_memory_data,
    synthesize_message,
    write_memory_data,
)


async def should_respond_to_message(event: MessageEvent, bot: Bot) -> bool:
    """根据配置和消息事件判断是否需要回复"""

    message = event.get_message()
    message_text = message.extract_plain_text().strip()

    # 如果不是群聊消息，直接返回 True
    if not isinstance(event, GroupMessageEvent):
        return True

    # 判断是否以关键字触发回复
    if config_manager.config.keyword == "at":  # 如果配置为 at 开头
        if event.is_tome():  # 判断是否 @ 了机器人
            return True
    elif message_text.startswith(config_manager.config.keyword):  # 如果消息以关键字开头
        return True

    # 判断是否启用了伪装人模式
    if config_manager.config.fake_people:
        # 如果是私聊消息且 @ 了机器人，直接返回 False
        if event.is_tome() and isinstance(event, PrivateMessageEvent):
            return False

        # 根据概率决定是否回复
        rand = random.random()
        rate = config_manager.config.probability
        if rand <= rate:
            return True

        # 获取内存数据
        memory_data: dict = get_memory_data(event)

        # 合成消息内容
        content = await synthesize_message(message, bot)

        # 获取当前时间戳
        Date = get_current_datetime_timestamp()

        # 获取用户角色信息
        role = (
            await bot.get_group_member_info(
                group_id=event.group_id, user_id=event.user_id
            )
        )["role"]
        if role == "admin":
            role = "群管理员"
        elif role == "owner":
            role = "群主"
        elif role == "member":
            role = "普通成员"

        # 获取用户 ID 和昵称
        user_id = event.user_id
        user_name = (
            await bot.get_group_member_info(
                group_id=event.group_id, user_id=event.user_id
            )
        )["nickname"]

        # 生成消息内容并记录到内存
        content_message = f"[{role}][{Date}][{user_name}（{user_id}）]说:{content}"
        memory_data["memory"]["messages"].append(
            {"role": "user", "content": content_message}
        )

        # 写入内存数据
        write_memory_data(event, memory_data)

    # 默认返回 False
    return False
