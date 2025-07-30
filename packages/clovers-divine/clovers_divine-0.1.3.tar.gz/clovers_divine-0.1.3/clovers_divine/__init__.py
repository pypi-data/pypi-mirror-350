import asyncio
from .clovers import Event, Result, create_plugin
from .daily_fortune import Manager as FortuneManager
from .tarot import Manager as TarotManager
from clovers.config import Config as CloversConfig
from .config import Config


config_data = CloversConfig.environ().setdefault(__package__, {})
__config__ = Config.model_validate(config_data)
config_data.update(__config__.model_dump())

fortune_manager = FortuneManager(
    data_path=__config__.daily_fortune_data,
    resource_path=__config__.daily_fortune_resorce,
    title_font=__config__.daily_fortune_title_font,
    text_font=__config__.daily_fortune_text_font,
)
tarot_manager = TarotManager(resource_path=__config__.tarot_resource)


def send_tarot_divine(result_list: list[Result]) -> Result: ...


if __config__.tarot_merge_forward:
    send_tarot_divine = lambda result_list: Result("merge_forward", result_list)
else:

    async def segmented_result(result_list: list[Result]):
        for result in result_list:
            yield result
            await asyncio.sleep(2)

    send_tarot_divine = lambda result_list: Result("segmented", segmented_result(result_list))


plugin = create_plugin()


@plugin.handle(["今日运势", "抽签", "运势"], ["group_id", "user_id"])
async def _(event: Event):
    user_id = event.user_id
    group_id = event.group_id or f"private:{user_id}"
    if image := fortune_manager.cache(group_id, user_id):
        text = "你今天在本群已经抽过签了，再给你看一次哦🤗"
    elif result := fortune_manager.get_results(user_id):
        text = "你今天已经抽过签了，再给你看一次哦🤗"
        image = fortune_manager.draw(group_id, user_id, result)
    else:
        text = "✨今日运势✨"
        result = fortune_manager.divine(user_id)
        image = fortune_manager.draw(group_id, user_id, result)
    return [Result("at", user_id), text, image]


@plugin.handle(["塔罗牌"], ["user_id"])
async def _(event: Event):
    card, explain, pic, flag = tarot_manager.tarot()
    event.properties["tarot"] = card
    theme = tarot_manager.random_theme()
    image = tarot_manager.draw(theme, pic, flag)
    return [Result("at", event.user_id), f"回应是{card}{explain}", image]


@plugin.handle(["占卜"], ["user_id"])
async def _(event: Event):
    tips, tarot_result_list = tarot_manager.divine()
    await event.call("text", f"启动{tips}，正在洗牌中...")
    theme = tarot_manager.random_theme()
    result_list = []
    infos = []
    for info, explain, pic, flag in tarot_result_list:
        infos.append(info)
        image = tarot_manager.draw(theme, pic, flag)
        if image:
            result_list.append(Result("list", [Result("text", f"{info}{explain}"), Result("image", image)]))
        else:
            result_list.append(Result("text", f"{info}{explain}"))
    event.properties["tarot"] = ",".join(infos)
    return send_tarot_divine(result_list)


__plugin__ = plugin
