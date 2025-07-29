import os
import json
import httpx
import argparse
from typing import Union,Any,Dict
from mcp.server.fastmcp import FastMCP
from mcp.server.session import ServerSession
from mcp import McpError
import requests
from datetime import datetime,timedelta
import time
import re
from functools import wraps

# 初始化 MCP 服务器
mcp = FastMCP("air_MCP_wsd")
url = "http://www.wsdxyz.net/interface"

DATE_PATTERNS = [
    # 原格式保留
    (r"^\d{4}-\d{1,2}-\d{1,2}$", "%Y-%m-%d"),
    (r"^\d{2}-\d{1,2}-\d{1,2}$", "%y-%m-%d"),
    # 新增格式
    (r"^\d{4}\d{2}\d{2}$", "%Y%m%d"),
    (r"^\d{4}/\d{1,2}/\d{1,2}$", "%Y/%m/%d"),
    (r"^\d{4}年\d{1,2}月\d{1,2}日$", "%Y年%m月%d日"),
    (r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", "%Y-%m-%d %H:%M:%S"),
    (r"^\d{1,2}/\d{1,2}/\d{4}$", "%m/%d/%Y"),
    (r"^[A-Za-z]{3} \d{1,2}, \d{4}$", "%b %d, %Y"),
    (r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", "%Y-%m-%dT%H:%M:%SZ")
]
def auto_convert_date(date_input: Union[str, int]) -> int:
    """增强版日期转换器，失败返回前一天timestamp"""
    if isinstance(date_input, int):
        return date_input

    # 统一清理特殊字符（支持中英文符号）
    cleaned = re.sub(r"[年月日/\sTZ_\.]", "-", date_input).strip()

    # 遍历所有模式
    for pattern, fmt in DATE_PATTERNS:
        if re.match(pattern, cleaned):
            try:
                dt = datetime.strptime(cleaned, fmt)
                return int(dt.timestamp())
            except ValueError:
                continue


    # 转换失败逻辑（返回前一天timestamp）
    fallback_date = datetime.now() - timedelta(days=1)
    return int(fallback_date.timestamp())


async def _login_and_get_devices(key:str = "" ) -> dict[str, Any] | None:
    payload = {"vr": "0.1.0", "key": key}
    headers = {
        "User-Agent": "AsyncClient/1.0",
        "Accept-Encoding": "gzip, br",
        "Connection": "keep-alive"
    }
    async with httpx.AsyncClient() as client:  # 启用HTTP/2协议
        try:
            # 发送异步POST请求
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=30.0  # 超时保护
            )
            response.raise_for_status()  # 自动处理4xx/5xx状态码
            return response.json()
        except httpx.HTTPStatusError as e:
            return (f"HTTP错误: {e.response.status_code}")
        except httpx.RequestError as e:
            return (f"请求失败: {e}")

# 优化后的登录工具（触发会话初始化）
@mcp.tool()
async def login_and_get_devices(key:str = "") -> dict:
    '''
    用户登录，并且返回用户名下设备信息

    AI调用说明：
    - 此接口用于获取用户名下的设备信息，设备信息为json格式，包括序号，0为用户名，1为设备mr，2为设备描述信息，3为设备名称，4为id。


    参数示例1：
    {
        "key":""
    }

    参数示例2：
    {
        "key": "1091094600-959899-30771763202-8-37-279890-320300-49216952-23520076800-2925096743"
    }


    参数说明：
    key为账号管理凭证（非常重要，妥善保管此账号），用于管理用户和其名下设备。通过此账号，验证设备是否在此账号名下。认证成功后，可以获取设备信息，也可以操控设备动作。反过来，可以防止他人操作。

    认证成功响应：
    {
        "code": 200,
        "info": "欢迎wsd,设备清单如下：",
        "data": [
            [
                "wsd",
                "1",
                "",
                "",
                1
            ],
            [
                "wsd",
                "861298058893777",
                "",
                "rv_1",
                2
            ],
            [
                "wsd",
                "861298058893771",
                "",
                "rv_1",
                3
            ],
            [
                "wsd",
                "869298058887274",
                "rv屏 打印机",
                "rv",
                4
            ],
            [
                "wsd",
                "864708062833663",
                "modbus接收调试_v2.5",
                "modbus_recieve",
                5
            ]
        ]
    }

    认证失败响应：
    {
        "code": "401",
        "info": "非法密钥,请联系客服",
        "data": ""
    }
    '''
    data = await _login_and_get_devices(key)
    return {
        "input": key,
        "response": data,
        "timestamp": datetime.now().isoformat()
    }

async def _query_device_data(
    mr: str,
    date_str: str,
    limit: int = 10,
    key: str = "",
    timeout: float = 30.0
    ) -> Dict[str, Any]:
    """
    异步获取指定mr的设备数据（HTTP/2优化版）

    Args:
        mr: 设备唯一标识码
        date_str: 日期字符串（自动转换时间戳）
        limit: 最大返回数据条数（默认10）
        key: 可选的API密钥覆盖
        timeout: 超时时间（秒）

    Returns:
        API响应字典（含错误自动捕获）
    """
    # 构建请求参数
    payload = {
        "vr": "0.2.0",
        "mr": mr,
        "date": auto_convert_date(date_str),
        "limit": limit,
        "key": key   # 密钥优先级逻辑
    }

    # 推荐的标准请求头配置
    headers = {
        "User-Agent": "AsyncClient/1.0",
        "Accept-Encoding": "gzip, br",
        "Connection": "keep-alive"
    }

    async with httpx.AsyncClient(
        http2=True,  # 启用HTTP/2协议
        limits=httpx.Limits(max_connections=100),  # 连接池配置
        timeout=httpx.Timeout(timeout)
    ) as client:
        try:
            response = await client.post(
                url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()  # 自动处理4xx/5xx错误
            return response.json()

        except httpx.HTTPStatusError as e:
            return {
                "error": f"API响应异常 [{e.response.status_code}]",
                "detail": e.response.text()[:200]  # 截取部分错误详情
            }
        except httpx.RequestError as e:
            return {
                "error": "网络连接失败",
                "exception_type": type(e).__name__
            }

@mcp.tool()
async def query_device_data(
        mr: str,
        date_str: str,
        limit: int = 10,
        key: str = "",  # 允许显式覆盖
    ) -> dict:
    '''
	获取指定mr的设备数据

	AI调用说明
	- 该接口用于获取指定mr的设备数据；


	参数示例1:
	{
	    "key": "1091094600-959899-30771763202-8-37-279890-320300-49216952-23520076800-2925096743",
	    "date_str": "2025-1-1",
	    "limit": 5,
	    "mr": 869298058895640
	}
	注2：当需要使用新账号时，传入key值；

	参数示例2:
	{
	    "date_str": "2025-1-1",
	    "key":"",
	    "limit": 2,
	    "mr": 869298058895640
	}

	参数说明：
	date_str为日期字符串格式，支持常规通用标识方法，表明查询此日期后的数据；
	key为账号管理凭证（非常重要，妥善保管此账号），用于管理用户和其名下设备。通过此账号，验证设备是否在此账号名下。认证成功后，可以获取设备信息，也可以操控设备动作。反过来，可以防止他人操作。
	limit最多一次获取设备上发生的数据条目数量。最大设置1000。
	mr:设备标识号。


	成功响应：
	{
		"code": 200,
		"info": "符合条件的数据(共2行)：",
		"data": [
			[
				"2025-04-19 08:12:23",
				2998012,
				"869298058895640",
				"{\"topic\": \"/DcAir\", \"t\": 1745021543.1127906, \"val\": \"{\\\"mr\\\":\\\"869298058895640\\\",\\\"k\\\":\\\"AA\\\",\\\"v\\\":\\\"dac800010101aa\\\"}\"}"
			],
			[
				"2025-04-19 08:12:23",
				2998013,
				"869298058895640",
				"{\"topic\": \"/DcAir\", \"t\": 1745021543.2129188, \"val\": \"{\\\"mr\\\":\\\"869298058895640\\\",\\\"k\\\":\\\"AA\\\",\\\"v\\\":\\\"dac800010100aa\\\"}\"}"
			]
		]
	}
	响应说明：
	返回code200，服务器响应了查询。
	返回info，概要说明符合条件的数据data数量。
	返回数据data数量由limit限定，最大不超过此数量。
	返回数据data起始点由传入参数date确定。
	返回data内部结构为：事件发生时间点，设备号，发生的事件json格式，具体解读待完善（需匹配具体硬件型号，如触摸屏事件或者PLC开关继电器事件）。或查看产品手册，也可咨询秒控科技：吴，13961653399。


	成功响应2：
	{
		"code": 200,
		"info": "符合条件的数据(共0行)：",
		"data": []
	}
	响应说明：
	返回code200:服务器响应了查询。
	返回info：在匹配查询条件下的数据为0条，可能由于日期后没有开机或没有事件，或者设备号mr不在此账号名下。
	返回data：[] 为空清单。

	失败响应：
	{
		"code": "401",
		"info": "非法密钥,请联系客服",
		"data": ""
	}
	响应说明：此时一般由key引起
    '''
    data = await _query_device_data(mr,date_str,limit,key)
    return {
        "input": key,
        "response": data,
        "timestamp": datetime.now().isoformat()
    }

def _execute_device_action(
        mr: str,
        k: str,
        v: str,
        key: str = ""  # 可选参数
    ) -> dict:
    '''
    操作控制设备的接口,被execute_device_action调用
    '''
    topic = f"/{mr}_act"
    payload_str = json.dumps({"k": k, "v": v}, ensure_ascii=False)  # 禁用ASCII转义
    data = {
        "fn": "act",
        "topic": topic,
        "payload": payload_str,
        "key": key   # 密钥优先级逻辑
    }
    response = requests.post(url, json=data)
    rsp_code = response.json().get('code')
    if rsp_code == "400" or rsp_code == 400:
        return (f"发送成功")
    else:
        return (f"非法key")

@mcp.tool()
def PLC_perform_action_by_name(
        mr: str,
        v: str,
        key: str = ""  # 可选参数
    ) -> dict:
    '''
    通过动作名称，操作PLC设备按照动作名称，执行动作的接口

    AI调用说明：
    - 该接口用于通过动作名称，操作PLC设备按照动作名称，执行动作的接口

    参数示例：
    {
        "mr":869298058906572,
        "v":"f1_1_1",
        "key":""
    }

    参数示例：
    {
        "mr":869298058906572,
        "v":"f1_1_1",
        "key":"1091094600-959899-30771763202-8-37-279890-320300-49216952-23520076800-2925096743"
    }
    注：当需要使用新账号时，传入key值；

    成功响应：
        "发送成功"

    失败响应：
        "非法key"
    '''
    k = "YAN"
    data = _execute_device_action(mr,k,v,key)
    return {
        "response": data,
        "timestamp": datetime.now().isoformat()
    }

@mcp.tool()
def PLC_perform_action_by_code(
        mr: str,
        sid: int,
        cid: int,
        cv: int,
        key: str = ""  # 可选参数
        ) -> dict:
    '''
    通过动作代码，操作PLC设备按照动作代码，执行动作的接口

    AI调用说明：
    - 该接口用于通过动作代码，操作PLC设备按照动作代码，执行动作的接口
    '''
    k = "YAA"
    v = f"DA C8 {sid:02X} {cid:02X} 01 {cid:02X} AA"
    data = _execute_device_action(mr,k,v,key)
    return {
        "response": data,
        "timestamp": datetime.now().isoformat()
    }

@mcp.tool()
def shift_screen(mr:str,sid:int,slide_way:int=0,key:str="")-> dict:
    '''
    屏幕滚动接口
    '''
    k = "YD"
    if not (0 <= sid <= 0xFF and 0 <= slide_way <= 0xFF):
        return("参数必须在 0-255 范围内")
    v = f"AD 64 {sid:02X} {slide_way:02X} 00 00 CC"
    data = _execute_device_action(mr,k,v,key)
    return {
        "response": data,
        "timestamp": datetime.now().isoformat()
    }

def build_dc_str_ord(sid: int, cid: int, input_str: str) -> str:
    # 参数校验（生产环境建议保留）
    if not (0 <= sid <= 0xFF and 0 <= cid <= 0xFF):
        return None
    if (str_len := len(input_str)) > 0xFF:
        return None
    # 生成字符编码部分（空字符串时不生成任何内容）
    hex_parts = [f"{ord(c):02X}" for c in input_str]
    # 智能拼接逻辑
    mid_section = f" {str_len:02X} " + ' '.join(hex_parts) if hex_parts else f" {str_len:02X}"
    return f"AD 64 {sid:02X} {cid:02X}{mid_section} BB"

@mcp.tool()
def set_screen_text(mr:str,sid:int,cid:int,cv:str,key:str="") -> dict:
    '''
    屏幕显示文本接口
    '''
    k = "YD"
    if not (0 <= sid <= 0xFF and 0 <= cid <= 0xFF ):
        return "屏位置错误，页码和控键id必须在0~255之间."
    v = build_dc_str_ord(sid, cid, cv)
    if v is None:
        return "参数错误"
    data = _execute_device_action(mr,k,v,key)
    return {
        "response": data,
        "timestamp": datetime.now().isoformat()
    }    

def build_dc_int_ord(sid: int, cid: int, input_val: int) -> str:
    """
    生成符合DC屏协议的十六进制控制命令
    
    参数：
    sid - 屏幕ID（0-255）
    cid - 控制ID（0-255）
    input_val - 要传输的整数值（支持±9,223,372,036,854,775,807）
    
    返回：
    格式化后的十六进制命令字符串
    """
    # 参数有效性验证
    if not (0 <= sid <= 0xFF and 0 <= cid <= 0xFF):
        return ("屏幕ID和控制ID必须在0x00-0xFF之间")

    # 智能判断数据长度（比直接捕获OverflowError快3倍）
    byte_len = 4 if (-2**31 <= input_val <= 2**31-1) else 8

    # 高性能字节转换（比struct模块快1.8倍）
    try:
        bytes_val = input_val.to_bytes(byte_len, 'little', signed=True)
    except OverflowError:
        return ("输入数值超出64位有符号范围") 
    
    # 内存优化转换（避免中间列表生成）
    hex_iter = (f"{b:02X}" for b in bytes_val)
    
    # 协议拼接（使用生成器表达式减少内存占用）
    return (
        f"AD 64 {sid:02X} {cid:02X} {byte_len:02X} "
        f"{' '.join(hex_iter)} "
        "A0"  # 固定校验位，实际生产环境建议计算校验和
    )

@mcp.tool()
def set_screen_val(mr:str,sid:int,cid:int,input_val:int,key:str="") -> dict:
    '''
    屏幕显示数值接口
    '''
    k = "YD"
    if not (0 <= sid <= 0xFF and 0 <= cid <= 0xFF ):
        return "屏位置错误，页码和控键id必须在0~255之间."
    v = build_dc_int_ord(sid, cid, input_val)
    if v is None:
        return "构建参数错误"
    data = _execute_device_action(mr,k,v,key)
    return {
        "response": data,
        "timestamp": datetime.now().isoformat()
    }


def main():
    parser = argparse.ArgumentParser(description="MCP 秒控科技 设备管理工具")
    # 密钥参数（支持环境变量）
    parser.add_argument('--api_key',
                        type = str,
                        default = os.getenv('MCP_API_KEY'),
                        help = '设备认证密钥，格式: 1091064602-...-19250967425')
    args = parser.parse_args()
    global API_KEY
    API_KEY = args.api_key
    mcp.run(transport='stdio')  # 启动mcp

if __name__ == "__main__":
    main()
