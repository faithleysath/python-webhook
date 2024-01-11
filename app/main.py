import os
import sys

from typing import List

from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

# 环境变量导入
ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("ACCESS_KEY_SECRET")
REDIR_RR_ID = os.environ.get("REDIR_RR_ID")
REDIR_RR = os.environ.get("REDIR_RR")
REDIR_RR_VALUE = os.environ.get("REDIR_RR_VALUE")
SRV_RR_ID = os.environ.get("SRV_RR_ID")
SRV_RR = os.environ.get("SRV_RR")
SRV_RR_VALUE = os.environ.get("SRV_RR_VALUE")
QB_USERNAME = os.environ.get("QB_USERNAME", "admin")
QB_PASSWORD = os.environ.get("QB_PASSWORD", "adminadmin")
QB_ADDR = os.environ.get("QB_ADDR", "127.0.0.1:8080")
DEFAULT_URL = os.environ.get("DEFAULT_URL", "https://www.baidu.com")

class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Alidns20150109Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Alidns
        config.endpoint = f'alidns.cn-hangzhou.aliyuncs.com'
        return Alidns20150109Client(config)

    @staticmethod
    def main(
        record_id: str,
        rr: str,
        type: str,
        value: str,
    ) -> None:
        client = Sample.create_client(access_key_id=ACCESS_KEY_ID, access_key_secret=ACCESS_KEY_SECRET)
        update_domain_record_request = alidns_20150109_models.UpdateDomainRecordRequest(
            record_id=record_id,
            rr=rr,
            type=type,
            value=value
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            print(client.update_domain_record_with_options(update_domain_record_request, runtime), "\n")
        except Exception as error:
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    @staticmethod
    async def main_async(
        record_id: str,
        rr: str,
        type: str,
        value: str,
    ) -> None:
        client = Sample.create_client(access_key_id=ACCESS_KEY_ID, access_key_secret=ACCESS_KEY_SECRET)
        update_domain_record_request = alidns_20150109_models.UpdateDomainRecordRequest(
            record_id=record_id,
            rr=rr,
            type=type,
            value=value
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.update_domain_record_with_options_async(update_domain_record_request, runtime)
        except Exception as error:
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

# 基于FastAPI的Webhook服务
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI(docs_url=None, redoc_url=None)

# 动态解析url转发
@app.get("/update_redir/{port}")
async def update(port: int):
    Sample.main(REDIR_RR_ID, REDIR_RR, "REDIRECT_URL", f"{REDIR_RR_VALUE}:{port}")
    return {"message": "Update Success"}

# srv解析
@app.get("/update_srv/{port}")
async def update(port: int):
    Sample.main(SRV_RR_ID, SRV_RR, "SRV", f"0 0 {port} {SRV_RR_VALUE}")
    return {"message": "Update Success"}

# url跳转
@app.get("/{tail:path}")
async def read_items(request: Request, tail: str = ''):
    # 获取当前URL
    current_url = str(request.url)

    # 获取domain, port, prefix和url
    domain = request.url.hostname
    # domain消去一级
    domain = '.'.join(domain.split('.')[1:])
    port = request.url.port
    pathnames = request.url.path.split('/')
    prefix = pathnames[1]
    # 若prefix为空，则跳转到DEFAULT_URL
    if prefix == '':
        return RedirectResponse(url=DEFAULT_URL, status_code=301)
    url = '/'.join(pathnames[2:])

    # 构造新的URL
    new_url = f"https://{prefix}.{domain}:{port}/{url}"

    # 重定向到新的URL
    response = RedirectResponse(url=new_url, status_code=302)
    return response