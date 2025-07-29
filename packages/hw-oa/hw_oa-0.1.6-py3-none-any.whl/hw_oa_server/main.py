import re
from typing import Any
import json
import logging

from mcp.server.fastmcp import FastMCP

from hw_oa_server.service import *
from hw_oa_server.service.account import get_user_id_by_account
from hw_oa_server.service.http_service import HttpService

logger = logging.getLogger(__name__)


# Initialize FastMCP server
mcp = FastMCP("hwoa-mcp-server", port=9000, host="0.0.0.0")


@mcp.prompt()
def server_prompt():
    return "你是一个OA系统，请根据用户的任务，调用合适的API接口，完成任务，并返回结果。"

@mcp.tool()
async def submit_leave_request (
    eeAccount: str,
    leaveType: int,
    title: str,
    leaveRemark: str|None,
    travelArea: str|None,
    startTime: str,
    endTime: str,
    timeSpan: float,
    approver: str,
    goOutType: str,
    isAssign: str,

) -> str:
    """提交请假或者外出申请, 提交前需要确保审批人、开始时间、结束时间、请假标题等信息存在，并且确保该请假时间段没有其他请假信息。
       返回提交结果。

    Args:
        eeAccount: 申请人账号
        leaveType: 请假类型，1-外出，2-事假。如果不是这些类型，返回不支持的请假类型。
        title: 标题，请假标题或请假原因
        leaveRemark: 备注可以为空，如果请假原因太长，则把详细原因写入到备注项。
        travelArea: 外出地点，请假类型为事假时，不需要填写外出地点。请假类型为外出时，如果用户没有填写外出地点，则默认为广州。
        startTime: 开始时间，通过问题判断，格式：2025-01-10 09:00:00
        endTime: 结束时间，通过问题判断，格式：2025-01-10 18:00:00
        timeSpan: 时长，可以为空。如果用户没有输入，请计算开始时间和结束时间的差值，每天的差值最大为7.5小时，中午12点半到14点为休息时间，不计入差值。
        approver: 审批人，如果用户没有输入，请默认为“刘晓玲”。
        goOutType: 外出类型，1-现场服务，2-沟通交流，3-其他。
        isAssign: 是否指派，1-是，0-否。默认为0。
    """

    logger.info(f"submit_leave_request............")

    # 业务逻辑处理
    time_format = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    if not re.match(time_format, startTime):
        raise ValueError("开始时间格式不符合要求，应为YYYY-MM-DD HH:mm:ss")

    if not re.match(time_format, endTime):
        raise ValueError("结束时间格式不符合要求，应为YYYY-MM-DD HH:mm:ss")
    
    if approver is None or approver == "":
        result = {"mcpCode": -1, "mcpMsg": "审批人不能为空"}
        return json.dumps(result, ensure_ascii=False)
    
    query_res, user_id, err_msg = get_user_id_by_account(approver)
    if query_res == 1:
        nextHandleEeId = user_id
    else:
        result = {"mcpCode": query_res, "mcpMsg": err_msg}
        logger.info("get_user_id_by_account result:::::%s",result)
        return json.dumps(result, ensure_ascii=False)

    API_URL = f"{HW_OA_API_URL}/hwoa/api/external/hw_assistant/leave_record_save"
    
    payload = {
        "app_name": APP_NAME,
        "app_secret": APP_SECRET,
        #"eeId": eeId,
        "domainAccount": eeAccount,
        "leaveType": leaveType,
        "goOutType": goOutType,
        "isAssign": isAssign,
        "title": title,
        "travelArea": travelArea,
        "leaveRemark": leaveRemark,
        "startTime": startTime,
        "endTime": endTime,
        "timeSpan": timeSpan,
        "nextHandleEeId": nextHandleEeId,
        "agentNames": ""
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    logger.info("submit_leave_request payload:::::%s",payload)
    print('submit_leave_request payload:::::%s',payload)

    # 
    result = await HttpService.sendHtppPostRequest(API_URL, payload, headers, "提交请假申请")
    return json.dumps(result, ensure_ascii=False)   



# 不用注解的方法添加工具
def add_tools(mcp: FastMCP):
    #mcp.add_tool(get_alerts)
    #mcp.add_tool(get_alerts1, name="get_alerts1", description="Get 中国气象局 alerts for a CN state.")
    pass

def main():
    print("Server running")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
