from nonebot import logger
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, MessageEvent
from nonebot.matcher import Matcher

from ..config import config_manager
from ..utils import get_memory_data, write_memory_data


async def del_memory(bot: Bot, event: MessageEvent, matcher: Matcher):
    """处理删除记忆的指令"""
    # 检查功能是否启用
    if not config_manager.config.enable:
        matcher.skip()

    # 如果是群聊事件
    if isinstance(event, GroupMessageEvent):
        # 获取群成员信息
        member = await bot.get_group_member_info(
            group_id=event.group_id, user_id=event.user_id
        )

        # 检查用户权限，非管理员或不在管理员列表的用户无法执行
        if (
            member["role"] == "member"
            and event.user_id not in config_manager.config.admins
        ):
            await matcher.send("你没有权限执行此操作（需要管理员权限）")
            return

        # 获取群聊记忆数据
        GData = get_memory_data(event)

        # 清除群聊上下文
        if GData["id"] == event.group_id:
            GData["memory"]["messages"] = []
            await matcher.send("群聊上下文已清除")
            write_memory_data(event, GData)
            logger.info(f"{event.group_id} 的记忆已清除")

    else:
        # 获取私聊记忆数据
        FData = get_memory_data(event)

        # 清除私聊上下文
        if FData["id"] == event.user_id:
            FData["memory"]["messages"] = []
            await matcher.send("私聊上下文已清除")
            logger.info(f"{event.user_id} 的记忆已清除")
            write_memory_data(event, FData)
