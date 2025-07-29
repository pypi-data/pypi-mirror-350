"""
账户服务
同步方法
"""

import httpx
import logging

from hw_oa_server.service import HW_OA_API_URL,APP_NAME,APP_SECRET # 子进程没有设置环境变量

logger = logging.getLogger(__name__)

def get_user_id_by_account(account: str) -> tuple[int,int,str]: # 返回:处理是否成功、用户ID、错误信息 
    """通过账号获取用户ID.

    Args:
        account: 账号
    """
    url = f"{HW_OA_API_URL}/hwoa/api/external/hw_assistant/leave_record_common_list"

    payload = {
        "app_name": APP_NAME,
        "app_secret": APP_SECRET,
        "leaveType": 1
        }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    with httpx.Client() as client:
        try:
            response = client.post(
                url=url, 
                json=payload,
                headers=headers, 
                timeout=5.0
            )
            response.raise_for_status()

            json_data = response.json()
            logger.info("response json_data:::::%s",json_data)
            if json_data.get("code") == 0:
                approver_list = json_data.get("data", {}).get("assigneeRespDto", {}).get("lstItem", [])
                # 查找匹配的审批人姓名
                for approver in approver_list:
                    if approver.get("eeName") == account:
                        return 1, approver.get("eeId"), "OK"
            
            return 0, -1, f"系统找不到该审批人: {account}"

        except Exception as e:
            return -1, -1, f"查询审批人失败: {str(e)}"



