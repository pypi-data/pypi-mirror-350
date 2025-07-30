from nonebot import logger
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.matcher import Matcher

from ..config import config_manager
from ..utils import get_memory_data, write_memory_data


async def disable(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    """处理禁用聊天功能的异步函数"""
    if not config_manager.config.enable:
        matcher.skip()  # 如果功能未启用，跳过处理

    # 获取群成员信息
    member = await bot.get_group_member_info(
        group_id=event.group_id, user_id=event.user_id
    )

    # 检查是否为普通成员且不在管理员列表中
    if member["role"] == "member" and event.user_id not in config_manager.config.admins:
        await matcher.send("你没有这样的权限哦～（需要管理员权限）")
        return

    # 记录禁用操作日志
    logger.debug(f"{event.group_id} disabled")

    # 获取并更新群聊状态数据
    data = get_memory_data(event)
    if data["id"] == event.group_id:
        if not data["enable"]:
            await matcher.send("聊天功能已禁用")
        else:
            data["enable"] = False
            await matcher.send("聊天功能已成功禁用")

    # 保存更新后的群聊状态数据
    write_memory_data(event, data)
