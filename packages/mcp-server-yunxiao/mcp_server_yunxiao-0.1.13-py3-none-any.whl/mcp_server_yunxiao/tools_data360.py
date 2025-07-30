from typing import Annotated, Optional, List
from pydantic import Field
from .client import _call_api
from . import mcp
import json

@mcp.tool(description="查询配额信息")
def query_quota(
    region: Annotated[str, Field(description="地域")],
    app_id: Annotated[Optional[List[str]], Field(description="用户AppID列表")],
    pay_mode: Annotated[Optional[List[str]], Field(description="计费模式列表，可选值：POSTPAID_BY_MONTH(包年包月), PREPAID(预付费), POSTPAID_BY_HOUR(按量计费), CDHPAID(CDH), SPOTPAID(竞价), POSTPAID_UNDERWRITE, CDCPAID, CHCPAID, UNDERWRITE")] = None,
    instance_family: Annotated[Optional[List[str]], Field(description="机型族列表")] = None,
    instance_type: Annotated[Optional[List[str]], Field(description="实例类型列表")] = None,
    limit: Annotated[int, Field(description="页长度，默认20")] = 100,
    offset: Annotated[int, Field(description="偏移量，默认0")] = 0,
    product_code: Annotated[str, Field(description="产品码")] = "cvm-instance",
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None,
    zone_id: Annotated[Optional[List[int]], Field(description="可用区ID列表")] = None,
    customhouse: Annotated[Optional[List[str]], Field(description="境内外列表，可选值：境内/境外")] = None,
) -> str:
    """查询配额信息
    
    Args:
        region: 地域
        product_code: 产品码
        limit: 页长度，默认20
        offset: 偏移量，默认0
        region_alias: 地域别名
        zone_id: 可用区ID列表
        app_id: 用户AppID列表
        pay_mode: 计费模式列表
        instance_type: 实例类型列表
        instance_family: 机型族列表
        customhouse: 境内外列表，可选值：境内/境外
        
    Returns:
        str: 配额信息的JSON字符串
    """
    params = {
        "region": region,
        "productCode": product_code,
        "limit": limit,
        "offset": offset
    }
    if region_alias is not None:
        params["regionAlias"] = region_alias
    if zone_id is not None:
        params["zoneId"] = zone_id
    if app_id is not None:
        params["appId"] = app_id
    if pay_mode is not None:
        params["payMode"] = pay_mode
    if instance_type is not None:
        params["instanceType"] = instance_type
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if customhouse is not None:
        params["customhouse"] = customhouse
    return _call_api("/data360/quota/query", params)

@mcp.tool(description="查询机型族信息")
def query_instance_families(
    instance_family: Annotated[Optional[str], Field(description="实例族名称")] = None,
    states: Annotated[Optional[List[str]], Field(description="实例族状态列表")] = None,
    supply_states: Annotated[Optional[List[str]], Field(description="实例族供货状态列表")] = None,
    instance_categories: Annotated[Optional[List[str]], Field(description="实例分类列表")] = None,
    type_names: Annotated[Optional[List[str]], Field(description="类型名称列表")] = None,
    instance_class: Annotated[Optional[str], Field(description="实例类型分类")] = None,
    page_number: Annotated[int, Field(description="页码")] = 1,
    page_size: Annotated[int, Field(description="每页数量")] = 20
) -> str:
    """查询机型族信息
    
    Args:
        instance_family: 实例族名称
        states: 实例族状态列表
        supply_states: 实例族供货状态列表
        instance_categories: 实例分类列表
        type_names: 类型名称列表
        instance_class: 实例类型分类
        page_number: 页码
        page_size: 每页数量
        
    Returns:
        查询结果的JSON字符串
    """
    params = {
        "pageNumber": page_number,
        "pageSize": page_size,
        "display": True
    }
    if instance_family:
        params["instanceFamily"] = instance_family
    if states:
        params["state"] = states
    if supply_states:
        params["supplyState"] = supply_states
    if instance_categories:
        params["instanceCategory"] = instance_categories
    if type_names:
        params["typeName"] = type_names
    if instance_class:
        params["instanceClass"] = instance_class
    return _call_api("/data360/instance-family", params)

@mcp.tool(description="查询实例数量")
def get_instance_count(
    region: Annotated[str, Field(description="地域")],
    next_token: Annotated[str, Field(description="分页token")] = "",
    limit: Annotated[int, Field(description="每页数量")] = 20,
    app_ids: Annotated[Optional[List[int]], Field(description="AppID列表")] = None,
    uins: Annotated[Optional[List[str]], Field(description="UIN列表")] = None,
    instance_types: Annotated[Optional[List[str]], Field(description="实例类型列表")] = None,
    instance_families: Annotated[Optional[List[str]], Field(description="实例族列表")] = None
) -> str:
    """查询实例数量
    
    Args:
        region: 地域
        next_token: 分页token
        limit: 每页数量
        app_ids: AppID列表
        uins: UIN列表
        instance_types: 实例类型列表
        instance_families: 实例族列表
        
    Returns:
        查询结果的JSON字符串
    """
    params = {
        "hasTotalCount": True,
        "nextToken": next_token,
        "limit": limit,
        "region": region
    }
    if app_ids:
        params["appId"] = app_ids
    if uins:
        params["uin"] = uins
    if instance_types:
        params["instanceType"] = instance_types
    if instance_families:
        params["instanceFamily"] = instance_families
    return _call_api("/data360/instance/count", params)

@mcp.tool(description="查询实例列表")
def query_instances(
    region: Annotated[str, Field(description="地域")],
    next_token: Annotated[str, Field(description="分页token")] = "",
    limit: Annotated[int, Field(description="每页数量")] = 20,
    app_ids: Annotated[Optional[List[int]], Field(description="AppID列表")] = None,
    uins: Annotated[Optional[List[str]], Field(description="UIN列表")] = None,
    instance_types: Annotated[Optional[List[str]], Field(description="实例类型列表")] = None,
    instance_families: Annotated[Optional[List[str]], Field(description="实例族列表")] = None
) -> str:
    """查询实例列表
    
    Args:
        region: 地域
        next_token: 分页token
        limit: 每页数量
        app_ids: AppID列表
        uins: UIN列表
        instance_types: 实例类型列表
        instance_families: 实例族列表
        
    Returns:
        查询结果的JSON字符串
    """
    params = {
        "hasTotalCount": True,
        "nextToken": next_token,
        "limit": limit,
        "region": region
    }
    if app_ids:
        params["appId"] = app_ids
    if uins:
        params["uin"] = uins
    if instance_types:
        params["instanceType"] = instance_types
    if instance_families:
        params["instanceFamily"] = instance_families
    return _call_api("/data360/instance", params)

@mcp.tool(description="查询实例详情")
def get_instance_details(
    region: Annotated[str, Field(description="地域")],
    instance_id: Annotated[Optional[List[str]], Field(description="实例ID")] = None
) -> str:
    """查询实例详情
    
    Args:
        region: 地域
        instance_id: 实例ID
        
    Returns:
        查询结果的JSON字符串
    """
    params = {
        "instanceId": instance_id,
        "region": region
    }
    return _call_api("/data360/instance/detail", params)

@mcp.tool(description="获取客户的预扣资源统计")
def get_user_owned_grid(
    app_id: Annotated[int, Field(description="APPID", gt=0)],
    region: Annotated[Optional[List[str]], Field(description="地域列表")] = None
) -> str:
    """获取用户拥有的预扣资源统计
    
    Args:
        app_id: APPID
        region: 地域列表
        
    Returns:
        str: 网格列表的JSON字符串
    """
    params = {
        "appId": app_id,
        "region": region
    }
    return _call_api("/data360/user360/grid", params)

@mcp.tool(description="获取客户的实例统计")
def get_user_owned_instances(
    app_id: Annotated[int, Field(description="APPID", gt=0)],
    region: Annotated[Optional[List[str]], Field(description="地域列表")] = None
) -> str:
    """获取用户拥有的实例资源统计
    
    Args:
        app_id: APPID
        region: 地域列表
        
    Returns:
        str: 实例列表的JSON字符串
    """
    params = {
        "appId": app_id,
        "region": region
    }
    return _call_api("/data360/user360/instance", params)

@mcp.tool(description="获取客户的账号信息")
def batch_query_customer_account_info(
    customer_ids: Annotated[List[str], Field(description="客户ID列表，可以是UIN和AppID")]
) -> str:
    """获取客户账号信息
    
    Args:
        customer_ids: 客户ID列表
        
    Returns:
        str: 客户账号信息的JSON字符串
    """
    return _call_api("/data360/customer/batch-query-account-info", customer_ids) 

@mcp.tool(description="获取客户的详细账号信息")
def get_customer_account_info(
    app_id: Annotated[List[int], Field(description="AppID")] = None,
    uin: Annotated[List[str], Field(description="Uin")] = None
) -> str:
    """获取客户账号信息
    
    Args:
        customer_ids: 客户ID列表
        
    Returns:
        str: 客户账号信息的JSON字符串
    """
    param = {}
    if app_id:
        param["appId"] = app_id
    if uin:
        param["uin"] = uin
    if not param:
        return json.dumps({ "errorMessage": "请传入有效的AppId或UIN。" }, ensure_ascii=False) 
    return _call_api("/data360/customer/account-info", param) 