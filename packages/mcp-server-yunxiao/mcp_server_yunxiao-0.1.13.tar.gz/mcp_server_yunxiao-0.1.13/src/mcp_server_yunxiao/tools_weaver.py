from typing import Annotated, Optional, List
from pydantic import Field
from .client import _call_api
from . import mcp
import json
from datetime import datetime

REGION_ALIAS_MAP = {
    "sheec": "ap-shenyang-ec",
    "sh": "ap-shanghai",
    "sao": "sa-saopaulo",
    "bjjr": "ap-beijing-fsi",
    "hzec": "ap-hangzhou-ec",
    "cgoec": "ap-zhengzhou-ec",
    "use": "na-ashburn",
    "xiyec": "ap-xian-ec",
    "cd": "ap-chengdu",
    "cq": "ap-chongqing",
    "shjr": "ap-shanghai-fsi",
    "szjr": "ap-shenzhen-fsi",
    "usw": "na-siliconvalley",
    "jkt": "ap-jakarta",
    "in": "ap-mumbai",
    "jnec": "ap-jinan-ec",
    "gz": "ap-guangzhou",
    "szsycft": "ap-shenzhen-sycft",
    "qyxa": "ap-qingyuan-xinan",
    "hk": "ap-hongkong",
    "sjwec": "ap-shijiazhuang-ec",
    "tpe": "ap-taipei",
    "gzopen": "ap-guangzhou-open",
    "jp": "ap-tokyo",
    "hfeec": "ap-hefei-ec",
    "qy": "ap-qingyuan",
    "bj": "ap-beijing",
    "whec": "ap-wuhan-ec",
    "csec": "ap-changsha-ec",
    "tsn": "ap-tianjin",
    "nj": "ap-nanjing",
    "de": "eu-frankfurt",
    "th": "ap-bangkok",
    "sg": "ap-singapore",
    "kr": "ap-seoul",
    "fzec": "ap-fuzhou-ec",
    "szx": "ap-shenzhen",
    "xbec": "ap-xibei-ec",
    "shadc": "ap-shanghai-adc",
    "shwxzf": "ap-shanghai-wxzf",
    "gzwxzf": "ap-guangzhou-wxzf",
    "szjxcft": "ap-shenzhen-jxcft",
    "shhqcft": "ap-shanghai-hq-cft",
    "shhqcftfzhj": "ap-shanghai-hq-uat-cft",
    "shwxzfjpyzc": "ap-shanghai-wxp-ops",
    "njxfcft": "ap-nanjing-xf-cft",
}

def _get_region_alias(region: str, region_alias: Optional[str] = None) -> str:
    """
    通用 region 到 regionAlias 的映射
    """
    if region_alias:
        return region_alias
    for k, v in REGION_ALIAS_MAP.items():
        if v == region:
            return k
    return ""

@mcp.tool(description="查询VStation任务列表（简称VS任务）")
def query_task_message(
    region: Annotated[str, Field(description="地域，如 ap-guangzhou")],
    task_id: Annotated[Optional[List[str]], Field(description="VStation任务ID")] = [],
    instance_id: Annotated[Optional[List[str]], Field(description="实例ID")] = [],
    uuid: Annotated[Optional[List[str]], Field(description="任务UUID")] = [],
    request_id: Annotated[Optional[List[str]], Field(description="请求ID")] = [],
    host_ip: Annotated[Optional[List[str]], Field(description="母机/宿主机的IP")] = [],
    owner: Annotated[Optional[List[str]], Field(description="客户Owner")] = [],
    start_time: Annotated[Optional[str], Field(description="起始时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    end_time: Annotated[Optional[str], Field(description="结束时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    limit: Annotated[int, Field(description="分页长度")] = 100,
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None
) -> str:
    """
    查询 VStation 任务列表
    Args:
        region: 地域，如 ap-guangzhou
        task_id: VStation任务ID
        instance_id: 实例ID
        uuid: 任务UUID
        request_id: 请求ID
        host_ip: 母机/宿主机 IP
        start_time: 起始时间，格式：YYYY-MM-DD HH:mm:ss（可选，默认当天 00:00:00）
        end_time: 结束时间，格式：YYYY-MM-DD HH:mm:ss（可选，默认当天 23:59:59）
        region_alias: 地域别名（可选，若未传则自动匹配）
    Returns:
        str: 查询结果的JSON字符串
    """
    # 自动补全时间
    if not start_time or not end_time:
        today = datetime.now().strftime("%Y-%m-%d")
        if not start_time:
            start_time = f"{today} 00:00:00"
        if not end_time:
            end_time = f"{today} 23:59:59"
    alias = _get_region_alias(region, region_alias)
    filters = []
    if task_id:
        filters.append({
            "Name": "task_id",
            "Values": task_id
        })
    if request_id:
        filters.append({
            "Name": "requestId",
            "Values": request_id
        })
    if uuid:
        filters.append({
            "Name": "uuid",
            "Values": uuid
        })
    if instance_id:
        filters.append({
            "Name": "uInstanceId",
            "Values": instance_id
        })
    if host_ip:
        filters.append({
            "Name": "hostIp",
            "Values": host_ip
        })
    if owner:
        filters.append({
            "Name": "owner",
            "Values": owner
        })
    params = {
        "Region": region,
        "Filters": filters,
        "StartTime": start_time,
        "EndTime": end_time,
        "Offset": 0,
        "Limit": limit,
        "Action": "QueryTaskMessage",
        "AppId": "251006228",
        "RequestSource": "YunXiao",
        "SubAccountUin": "493083759",
        "Uin": "493083759",
        "regionAlias": alias,
        "Fields": [
            "taskStatus",
            "code",
            "cursor",
            "errorMsg",
            "hostIp",
            "hypervisor",
            "mode",
            "owner",
            "parentTaskId",
            "region",
            "requestId",
            "startTime",
            "taskId",
            "taskName",
            "taskProgress",
            "taskState",
            "traceRequestId",
            "uInstanceId",
            "uuid",
            "finishTime",
            "updateTime",
            "delayExecSteps",
            "hasDelaySteps",
            "migrateHostIp",
            "stepsLength",
            "productCategory",
            "chcId",
            "dedicatedClusterId",
            "p2pFlow",
            "desTaskId",
            "dataDiskSerial",
            "rootDiskSerial",
            "vifSerial",
            "uImageId",
            "vpcId",
            "instanceType",
            "zoneId",
            "gridId"
        ]
    }
    return _call_api("/weaver/upstream/terra/QueryTaskMessage", params)

@mcp.tool(description="查询VStation错误码（VStation简称VS）")
def describe_error_codes(
    region: Annotated[str, Field(description="地域，如 ap-guangzhou")],
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None
) -> str:
    """
    查询 VStation 错误码
    Args:
        region: 地域，如 ap-guangzhou
        region_alias: 地域别名（可选，若未传则自动匹配）
    Returns:
        str: 查询结果的JSON字符串
    """
    alias = _get_region_alias(region, region_alias)
    params = {
        "Region": region,
        "AppId": "251006228",
        "Action": "DescribeErrorCodes",
        "Uin": "493083759",
        "SubAccountUin": "493083759",
        "RequestSource": "YunXiao",
        "regionAlias": alias
    }
    return _call_api("/weaver/upstream/terra/QueryTaskMessage", params)

@mcp.tool(description="查询母机Compute任务列表")
def describe_host_task(
    region: Annotated[str, Field(description="地域，如 ap-guangzhou")],
    host: Annotated[str, Field(description="宿主机IP")],
    vs_task_id: Annotated[int, Field(description="VStation任务ID")],
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None
) -> str:
    """
    查询 Compute 任务列表
    Args:
        region: 地域，如 ap-guangzhou
        host: 宿主机IP
        vs_task_id: VStation任务ID
        region_alias: 地域别名（可选，若未传则自动匹配）
    Returns:
        str: 查询结果的JSON字符串
    """
    alias = _get_region_alias(region, region_alias)
    params = {
        "TaskId": vs_task_id,
        "Host": host,
        "Region": region,
        "Action": "DescribeHostTask",
        "AppId": "251006228",
        "RequestSource": "QCLOUD_OP",
        "SubAccountUin": "493083759",
        "Uin": "493083759",
        "regionAlias": alias
    }
    return _call_api("/weaver/upstream/terra/DescribeHostTask", params)

@mcp.tool(description="查询母机Compute任务的执行日志")
def query_host_task_log(
    region: Annotated[str, Field(description="地域，如 ap-guangzhou")],
    host_ip: Annotated[str, Field(description="宿主机IP")],
    host_task_id: Annotated[str, Field(description="母机/宿主机/Compute组件的任务ID，为describe_host_task返回的taskid字段。注意这里不要和VS任务ID混淆。")],
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None
) -> str:
    """
    查询 Compute 任务的执行日志
    Args:
        region: 地域，如 ap-guangzhou
        host_task_id: 宿主机IP
        task_id: 母机/宿主机任务ID
        region_alias: 地域别名（可选，若未传则自动匹配）
    Returns:
        str: 查询结果的JSON字符串
    """
    alias = _get_region_alias(region, region_alias)
    params = {
        "TaskId": host_task_id,
        "HostIp": host_ip,
        "Region": region,
        "Action": "QueryTaskLog",
        "AppId": "1251783334",
        "RequestSource": "YunXiao",
        "SubAccountUin": "3205597606",
        "Uin": "3205597606",
        "regionAlias": alias
    }
    return _call_api("/weaver/upstream/terra/QueryTaskLog", params) 