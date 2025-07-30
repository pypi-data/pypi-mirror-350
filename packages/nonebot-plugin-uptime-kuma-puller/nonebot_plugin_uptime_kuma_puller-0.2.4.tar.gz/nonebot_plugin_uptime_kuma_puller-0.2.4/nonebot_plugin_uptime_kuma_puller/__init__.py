from nonebot import require
require("nonebot_plugin_waiter")
require("nonebot_plugin_alconna")
require("nonebot_plugin_group_config")
from nonebot.plugin import on_command
from datetime import datetime
import time
import aiohttp
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import At, Image, on_alconna, Field
from nonebot_plugin_group_config import GroupConfig, GetGroupConfig
from arclet.alconna import Args, Option, Alconna, Subcommand, store_true, CommandMeta, Arparma, count
from nonebot.adapters import Event
from nonebot.adapters import Bot
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot_plugin_waiter import suggest
from nonebot.log import logger
from string import Template
from enum import Enum

from nonebot import get_plugin_config
from .config import Config

class SupportAdapterModule(str, Enum):
    """支持的适配器的模块路径"""

    console = "nonebot.adapters.console"
    ding = "nonebot.adapters.ding"
    discord = "nonebot.adapters.discord"
    dodo = "nonebot.adapters.dodo"
    feishu = "nonebot.adapters.feishu"
    gewechat = "nonebot.adapters.gewechat"
    github = "nonebot.adapters.github"
    heybox = "nonebot.adapters.heybox"
    kritor = "nonebot.adapters.kritor"
    kook = "nonebot.adapters.kaiheila"
    mail = "nonebot.adapters.mail"
    milky = "nonebot.adapters.milky"
    minecraft = "nonebot.adapters.minecraft"
    mirai = "nonebot.adapters.mirai"
    ntchat = "nonebot.adapters.ntchat"
    onebot11 = "nonebot.adapters.onebot.v11"
    onebot12 = "nonebot.adapters.onebot.v12"
    qq = "nonebot.adapters.qq"
    red = "nonebot.adapters.red"
    satori = "nonebot.adapters.satori"
    telegram = "nonebot.adapters.telegram"
    tail_chat = "nonebot_adapter_tailchat"
    wxmp = "nonebot.adapters.wxmp"

__version__ = "0.2.4"

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_uptime_kuma_puller",
    description="This is a plugin that can generate a UptimeKuma status page summary for your Nonebot",
    type='application',
    usage="This is a plugin that can generate a UptimeKuma status page summary for your Nonebot",
    homepage=(
        "https://github.com/bananaxiao2333/nonebot-plugin-uptime-kuma-puller"
    ),
    config=Config,
    supported_adapters=set(SupportAdapterModule.__members__.values()),
    extra={},
)

logger.info(
    f"Initializing nonebot_plugin_uptime_kuma_puller version: {__version__}"
)

plugin_config = get_plugin_config(Config).ukp

#query_uptime_kuma = Alconna("健康", aliases={"uptime", "ukp"})
query_uptime_kuma_alc = Alconna(
    "uptime",
    Subcommand(
        "check|检查",
        Option("-n|--name|--名字|--项目", Args["name", str, Field(completion=lambda: "请输入项目名称"),], help_text="项目名称"),
        Option("-t|--time|--时间", action=count, default=0, help_text="是否显示查询用时"),
        help_text="检查指定项目状态"
    ),
    Option("list|列出", help_text="列出可查询项目"),
    meta = CommandMeta(
        fuzzy_match=True,
        description="检查项目列表各状态",
        author="bananaxiao2333"
    ),
)
query_uptime_kuma = on_alconna(query_uptime_kuma_alc, auto_send_output=True, use_cmd_start = True, comp_config={"lite": True}, skip_for_unmatch=False, aliases = {"健康", "ukp"})


def takeSecond(elem):
    return elem[1]

async def Query(proj_name, show_time):
    try:
        start_time = time.time() # 开始计时
        main_api = f"{plugin_config.query_url}/api/status-page/{proj_name}"
        heartbeat_api = f"{plugin_config.query_url}/api/status-page/heartbeat/{proj_name}"
        ret = ""
        msg = ""
        status_statistics = {}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(main_api) as response:
                if response.status != 200:
                    msg += f"Http error {response.status}"
                    return msg
                content_js = await response.json()

            async with session.get(heartbeat_api) as response:
                if response.status != 200:
                    msg += f"Http error {response.status}"
                    return msg
                heartbeat_content_js = await response.json()

        proj_title = content_js["config"]["title"]

        # 获取监控项名称列表pre
        pub_list = content_js["publicGroupList"]
        pub_list_ids = []
        for pub_group in pub_list:
            for pub_sbj in pub_group["monitorList"]:
                tag = ""
                if "tags" in pub_sbj and plugin_config.show_tags:
                    #print(pub_sbj)
                    if pub_sbj["tags"] != []:
                        tag = f"[{pub_sbj['tags'][0]['name']}]"
                pub_sbj_name = f"{tag}{pub_sbj['name']}"
                pub_list_ids.append([pub_sbj["id"], pub_sbj_name])

        # 查询每个监控项的情况pre
        heartbeat_list = heartbeat_content_js["heartbeatList"]
        ping_statistics_total_ping = 0
        ping_statistics_num = 0
        ping_statistics_max = 0
        ping_statistics_min_flag = False
        ping_statistics_min = 0
        ping_statistics_arvg = 0
        for i in range(len(pub_list_ids)):
            pub_sbj = pub_list_ids[i]
            heartbeat_sbj = heartbeat_list[str(pub_sbj[0])][-1]
            # 显示在线状况
            if heartbeat_sbj["status"] in plugin_config.status_mapping: # 检查状态
                status = plugin_config.status_mapping[heartbeat_sbj["status"]]
            else:
                status = plugin_config.status_mapping["unknow"]
            if heartbeat_sbj["status"] in status_statistics: # 进行项目统计
                status_statistics[heartbeat_sbj["status"]] = status_statistics[heartbeat_sbj["status"]] + 1
            else:
                status_statistics[heartbeat_sbj["status"]] = 1
            # 显示数字ping
            ping_is_not_none = heartbeat_sbj["ping"] is not None
            ping = f" {heartbeat_sbj['ping']}ms" if ping_is_not_none and plugin_config.show_ping else ""
            if ping_is_not_none:
                ping_statistics_total_ping += heartbeat_sbj['ping']
                ping_statistics_num += 1
                ping_statistics_max = heartbeat_sbj['ping'] if heartbeat_sbj['ping'] > ping_statistics_max else ping_statistics_max
                ping_statistics_min = heartbeat_sbj['ping'] if heartbeat_sbj['ping'] < ping_statistics_min else ping_statistics_min
                if not ping_statistics_min_flag: # 如果min值并未初始化
                    ping_statistics_min = heartbeat_sbj['ping']
                    ping_statistics_min_flag = True
            temp_txt = f"{status}{ping}"
            pub_list_ids[i].append(temp_txt)
        ping_statistics_arvg = round(ping_statistics_total_ping / ping_statistics_num if ping_statistics_num != 0 else 0, 1)

        # 获取公告
        incident_msg = ""
        if plugin_config.show_incident:
            incident = content_js["incident"]
            if incident is not None:
                style = str(incident["style"])
                title = str(incident["title"])
                content = str(incident["content"])
                # 读取更新时间（由于第一次创建不更新时会显示null所以需要下列判断）
                if incident["lastUpdatedDate"] == None:
                    u_time = str(incident["createdDate"])
                else:
                    u_time = str(incident["lastUpdatedDate"])
                # 可调配置项
                if plugin_config.show_incident_update_time:
                    incident_update_time = f"\n{plugin_config.incident_update_time_text}{u_time}"
                else:
                    incident_update_time = ""
                if style.lower() in plugin_config.incident_type_trans:
                    style = plugin_config.incident_type_trans[style]
                else:
                    style = style.upper()
                if plugin_config.show_incident_type:
                    incident_style = f"【{style}】"
                else:
                    incident_style = ""
                incident_template = Template(plugin_config.incident_template)
                incident_template_mapping = {
                    "incident_style":incident_style,
                    "title":title,
                    "content":content,
                    "incident_update_time_ret":incident_update_time,
                    "time":datetime.now()
                }
                incident_msg = incident_template.safe_substitute(incident_template_mapping)
            
        # 排序并生成监控项部分
        proj_msg = ""
        pub_list_ids.sort(key=takeSecond)
        for index, pub_sbj in enumerate(pub_list_ids):
            proj_msg += f"{pub_sbj[1]} {pub_sbj[2]}"
            if index != len(pub_list_ids) - 1:
                proj_msg += "\n"
        
        # 处理维护消息
        maintenance_list = []
        if plugin_config.show_maintenance:
            maintenance = content_js["maintenanceList"]
            if maintenance is not None:
                maintenance_msg = ""
                maintenance_msg_template = Template(plugin_config.maintenance_template)
                for index, value in enumerate(maintenance):
                    maintenance_msg_time = ""
                    maintenance_strategy_transed = value["strategy"]
                    if value["strategy"] in plugin_config.maintenance_time_template_list: # 注入维护时间区间
                        maintenance_msg_time_template = Template(plugin_config.maintenance_time_template_list[value["strategy"]])
                        maintenance_msg_time_mapping = {
                            "cron": value["cron"],
                            "duration": value["duration"],
                            "interval_day": value["intervalDay"],
                            "timezone": value["timezone"],
                            "timezone_offset": value["timezoneOffset"]
                        }
                        maintenance_msg_time = maintenance_msg_time_template.safe_substitute(maintenance_msg_time_mapping)
                    if value["strategy"] in plugin_config.maintenance_strategy_trans:
                        maintenance_strategy_transed = plugin_config.maintenance_strategy_trans[value["strategy"]]
                    maintenance_msg_mapping = { # 注入维护消息总成
                        "id": value["id"],
                        "title": value["title"],
                        "description": value["description"],
                        "strategy": maintenance_strategy_transed,
                        "maintenance_time": maintenance_msg_time
                    }
                    maintenance_msg += "\n" + maintenance_msg_template.safe_substitute(maintenance_msg_mapping)
        
        # 处理统计信息
        status_statistics_msg = ""
        for key, value in status_statistics.items():
            icon = plugin_config.status_mapping[key] # 获取图标
            status_statistics_msg_template = Template(plugin_config.status_statistics_template)
            status_statistics_msg_template_mapping = {
                "icon" : icon,
                "number" : status_statistics[key]
            }
            status_statistics_temp = status_statistics_msg_template.safe_substitute(status_statistics_msg_template_mapping)
            status_statistics_msg += status_statistics_temp
        #status_statistics_msg += str(status_statistics)
        ping_statistics_template = Template(plugin_config.ping_statistics_template)
        ping_statistics_template_mapping = {
            "argv" : ping_statistics_arvg,
            "max" : ping_statistics_max,
            "min" : ping_statistics_min
        }
        ping_statistics_msg = ping_statistics_template.safe_substitute(ping_statistics_template_mapping)

        end_time = time.time() #结束计时
        took_time = f"消耗时间{round(((end_time - start_time)*1000), 1)}ms"
        if not show_time:
            took_time = ""
        # 格式最后输出
        msg_template = Template(plugin_config.query_template)
        msg_template_mapping = {
            "title":proj_title,
            "proj_msg":proj_msg,
            "incident_msg":incident_msg,
            "maintenance_msg":maintenance_msg,
            "status_statistics_msg":status_statistics_msg,
            "ping_statistics_msg":ping_statistics_msg,
            "took_time":took_time,
            "time":datetime.now()
        }
        msg = msg_template.safe_substitute(msg_template_mapping)
    except Exception as e:
        msg = f"{plugin_config.error_prompt}\n{e}"
        raise e
    return msg

@query_uptime_kuma.handle()
async def _(matcher: Matcher,event: Event,args: Arparma):
    result = ""
    if args.find("check"):
        if args.name:
            proj_name = args.name.lower()
            if proj_name in plugin_config.proj_name_list:
                result = await Query(proj_name, show_time=bool(args.query("check.time.value")))
                await query_uptime_kuma.finish(result)
            else:
                result = f"可查询列表{plugin_config.proj_name_list}中不存在{proj_name}，请重试！"
                await query_uptime_kuma.finish(result)
        """
        proj_name = await suggest(f"{plugin_config.suggest_proj_prompt}", plugin_config.proj_name_list, retry=plugin_config.retry, timeout=plugin_config.timeout)
        if proj_name is None:
            await query_uptime_kuma.finish(f"{plugin_config.no_arg_prompt}")
        result = await Query(proj_name)
        await query_uptime_kuma.finish(result)
        """
    if args.find("list"):
        result = Template(plugin_config.ava_template).safe_substitute({
            "list" : plugin_config.proj_name_list
        })
        await query_uptime_kuma.finish(result)

logger.info(
    f"The nonebot_plugin_uptime_kuma_puller initialization has been completed. If no error is seen, it indicates that the initialization was successful"
)