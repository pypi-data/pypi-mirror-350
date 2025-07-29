# -*- coding: utf-8 -*-
import hashlib
import json
import logging
import os
import random
import time
from typing import Optional, Annotated
import asyncio

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import Field

logger = logging.getLogger("mcp")

# 初始化mcp服务
mcp = FastMCP("btrip-mcp-server")


def signature(timestamp: str, nonce: str, req_body: str, encrypt_key: str) -> str:
    # 参数校验
    if not all(isinstance(arg, str) for arg in [timestamp, nonce, req_body, encrypt_key]):
        raise TypeError("所有参数必须为字符串类型")

    # 拼接顺序必须与Java保持一致
    raw_str = f"{timestamp}{nonce}{encrypt_key}{req_body}"

    # 创建SHA-256对象（推荐用new方式提升复用性）
    sha = hashlib.sha256()
    sha.update(raw_str.encode('utf-8'))  # 必须指定编码

    # 返回小写十六进制字符串（与Java兼容）
    return sha.hexdigest()


async def execute(body: object, url: str):
    # api_secret_key = os.getenv("api_secret_key")
    api_secret_key = "21f7ca190505455fb4215ae4e09cb4c6"
    if not api_secret_key:
        return "请先设置aes_key环境变量"

    timestamp = int(time.time() * 1000)
    nonce = ''.join(random.choices('0123456789', k=6))
    sign = signature(str(timestamp), nonce, json.dumps(body, ensure_ascii=False, separators=(',', ':')), api_secret_key)

    logger.info("认证数据打印,timestamp:{} nonce:{} body:{} sign:{}".format(timestamp, nonce, json.dumps(body), sign))

    headers = {"Content-Type": "application/json; charset=utf-8", "x-sailing-timestamp": str(timestamp),
               "x-sailing-nonce": nonce, "x-sailing-signature": sign}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.post(url, json=body)
        if response.status_code != 200:
            return "查询失败"

        response.encoding = 'utf-8'
        logger.info("返回数据, body:{}".format(response.text))
        return response.text


@mcp.tool(name="查询企业员工部门信息",
          description="查询企业员工部门信息接口，输入企业id和员工id，返回该员工的所属部门信息")
async def query_employee_org(corpId: str = Field(description="要查询员工所属企业id"),
                             employeeId: str = Field(description="要查询的员工的 id")) -> object:
    logger.info("收到查询员工组织请求, corpId:{} employeeId:{}".format(corpId, employeeId))

    body = {"corpId": corpId, "employeeId": employeeId}
    url = "https://sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryEmployeeOrg"
    return await execute(body, url)


@mcp.tool(name="查询城市信息",
          description="搜索城市信息，输入城市关键词，返回城市相关的信息")
async def standard_search(keyword: str = Field(description="城市搜索的关键词,支持模糊搜索,必填参数"),
                          queryCityType: Optional[str] = Field(None,
                                                               description="查询城市类型 flight: 机票 、train: 火车 、 hotel: 酒店; 非必填"),
                          searchType: Optional[str] = Field(None,
                                                            description="查询城市类型 flight: 机票 、train: 火车 、 hotel: 酒店; 非必填")) -> object:
    logger.info(
        "收到查询城市信息请求, keyword:{} queryCityType:{} searchType:{}".format(keyword, queryCityType, searchType))

    body = {"keyword": keyword, "queryCityType": queryCityType, "searchType": searchType}
    url = "https://sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/standardSearch"
    return await execute(body, url)


@mcp.tool(name="批量查询员工信息",
          description="批量查询员工信息, 输入企业id和员工id列表,返回员工信息集合")
async def query_employee_list_by_employee_id_list(corpId: str = Field(description="企业id,必填参数"),
                                                  employeeIdList: [] = Field(
                                                      description="员工id列表,必填参数"), ) -> object:
    logger.info("收到批量查询员工信息列表, corpId:{} employeeIdList:{}".format(corpId, employeeIdList))

    body = {"corpId": corpId, "employeeIdList": employeeIdList}
    url = "https://sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryEmployeeListByEmployeeIdList"
    return await execute(body, url)


@mcp.tool(name="查询员工的基本信息",
          description="查询员工的基本信息	, 输入企业id和员工id,返回员工基本信息")
async def query_employee_basic(corpId: str = Field(description="企业id,必填参数"),
                               employeeId: str = Field(description="员工id,必填参数"), ) -> object:
    logger.info("收到查询员工的基本信息, corpId:{} employeeId:{}".format(corpId, employeeId))

    body = {"corpId": corpId, "employeeId": employeeId}
    url = "https://sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryEmployeeBasic"
    return await execute(body, url)


@mcp.tool(name="查询员工的可用发票抬头信息列表",
          description="查询员工的可用发票抬头信息列表, 输入企业id和员工id,返回员工可用的发票抬头信息列表")
async def select_user_valid_invoice(corpId: str = Field(description="企业id,必填参数"),
                                    employeeId: str = Field(description="员工id,必填参数"), ) -> object:
    logger.info("收到查询员工的可用发票抬头信息列表, corpId:{} employeeId:{}".format(corpId, employeeId))

    body = {"corpId": corpId, "dingUserId": employeeId}
    url = "https://sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/selectUserValidInvoice"
    return await execute(body, url)


@mcp.tool(name="基于关键字搜索员工发票抬头信息列表",
          description="基于关键字搜索员工发票抬头信息列表, 输入企业id和员工id和发票抬头关键字,返回员工搜索出的可用的发票抬头信息列表")
async def query_invoice_list(corpId: str = Field(description="企业id,必填参数"),
                             employeeId: str = Field(description="员工id,必填参数"),
                             keyword: Optional[str] = Field(None,
                                                            description="发票抬头搜索关键字,必填参数"), ) -> object:
    logger.info(
        "收到基于关键字搜索员工发票抬头信息列表, corpId:{} employeeId:{} keyword:{}".format(corpId, employeeId,
                                                                                            keyword))

    body = {"corpId": corpId, "userIdList": [employeeId], "keyword": keyword}
    url = "https://sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryInvoiceList"
    return await execute(body, url)


@mcp.tool(name="基于关键字搜索员工可用的成本中心信息列表",
          description="基于关键字搜索员工可用的成本中心信息列表, 输入企业id和员工id,成本中心关键字,返回员工可用的成本中心信息列表")
async def query_cost_centers(corpId: str = Field(description="企业id,必填参数"),
                             employeeId: str = Field(description="员工id,必填参数"),
                             title: Optional[str] = Field(None,
                                                          description="成本中心关键字,非必填参数,不传默认查询员工所有的成本中心列表"),
                             numLimit: int = Field(10,
                                                   description="成本中心列表返回的最大数量,非必填,默认10")) -> object:
    logger.info(
        "收到查询员工可用的成本中心信息, corpId:{} employeeId:{} title:{} numLimit:{}".format(corpId, employeeId,
                                                                                              title, numLimit))

    body = {"corpId": corpId, "userId": employeeId, "title": title, "numLimit": numLimit}
    url = "https://sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryCostCenters"
    return await execute(body, url)


@mcp.tool(name="基于项目关键字搜索员工可用的项目信息列表",
          description="基于项目关键字搜索员工可用的项目信息列表, 输入企业id和员工id 可选输入项目名称关键字,返回员工可用的项目信息列表")
async def query_projects(corpId: str = Field(description="企业id,必填参数"),
                         employeeId: str = Field(description="员工id,必填参数"),
                         projectName: Optional[str] = Field(None,
                                                            description="项目名称关键字, 不传查询员工所有可用的项目信息列表,非必填参数"),
                         projectNumLimit: int = Field(10,
                                                      description="成本中心列表返回的最大数量,非必填,默认10")) -> object:
    logger.info(
        "收到基于项目关键字搜索员工可用的项目信息列表, corpId:{} employeeId:{} projectName:{} projectNumLimit:{}".format(
            corpId, employeeId,
            projectName,
            projectNumLimit))

    body = {"corpId": corpId, "userId": employeeId, "projectName": projectName, "projectNumLimit": projectNumLimit}
    url = "https://sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryProjects"
    return await execute(body, url)


@mcp.tool(name="对生成的表单做校验",
          description="对生成的表单做校验")
async def query_projects(corpId: str = Field(description="企业id,必填参数"),
                         employeeId: str = Field(description="员工id,必填参数"),
                         schema: str = Field(description="表单Schema"),
                         formData: str = Field(description="表单数据"),
                         templateCode: str = Field(description="模板Code")) -> object:
    logger.info("对生成的表单做校验, corpId:{} employeeId:{} schema:{} formData:{} templateCode:{}".format(
        corpId, employeeId, schema, formData, templateCode))

    body = {"corpId": corpId, "employeeId": employeeId, "schema": schema, "formData": formData,
            "templateCode": templateCode}
    url = "https://pre-sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/checkForm"
    return await execute(body, url)


def run():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
