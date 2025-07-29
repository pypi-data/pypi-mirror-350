import httpx
import logging

logger = logging.getLogger(__name__)

class HttpService:
    def __init__(self):
        self.url = "http://v-test85-centos7:8080/api/v1/leave/submit"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def sendHtppPostRequest(url: str, payload: dict, headers: dict,title: str="请求"):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                logger.info("response json_data:::::%s", json_data)
                #mcpCode=1表示正常结束，0表示异常但可以修复，-1表示异常无法修复了
                if json_data.get("code") == 0:
                    result = {"mcpCode": 1, "mcpMsg": f"{title}成功"}
                else:
                    logger.info("sendHtppPostRequest error:::::%s",json_data.get("msg"))
                    result = {"mcpCode": 0, "mcpMsg": json_data.get("msg")}

                return result

            except Exception as e:
                logger.info("sendHtppPostRequest error:::::%s",e)
                result = {"mcpCode": -1, "mcpMsg": f"{title}失败: {str(e)}"}
                return result
