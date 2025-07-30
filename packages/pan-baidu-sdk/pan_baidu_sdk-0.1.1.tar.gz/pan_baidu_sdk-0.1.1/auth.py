import openapi_client as openapi_client
from openapi_client.api import auth_api
from pprint import pprint
import requests


class AuthApi:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        pass

    def oauthtoken_devicecode(self):
        """
        devicecode
        get device code 获取设备码
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = auth_api.AuthApi(api_client)
          
            scope = "basic,netdisk"  # str |

            try:
                api_response = api_instance.oauth_token_device_code(self.client_id, scope)
                pprint(api_response)

                """
                {
                    device_code: "984c2459ec4140137a017fc49",
                    user_code: "8drp666k",
                    verification_url: "https://openapi.baidu.com/device",
                    qrcode_url: "https://openapi.baidu.com/device/qrcode/a526130da5e45870872317478/8drp69hk",
                    expires_in: 300,
                    interval: 5
                }

                选择以下两种方式之一引导用户授权:
                (1)扫二维码方式授权在上一步,您同时获取到了一个二维码url(qrcode_url).
                您根据返回的二维码url展示给用户二维码,用户通过手机等智能终端扫描二维码(如百度app扫码,百度网盘扫码,微信扫码等),使用百度帐号完成授权.

                (2)输入用户码方式授权在上一步,您获取到了用户码 user code,同时获取到了授权url(verification_url).
                您展示用户码给用户,展示授权url提供的页面给用户,用户在该页面输入用户码完成授权.

                """

                return api_response

            except openapi_client.ApiException as e:
                print(
                    "Exception when calling AuthApi->oauth_token_device_code: %s\n" % e
                )

    def oauthtoken_devicetoken(self, device_code):
        """
        get token by device code 通过设备码获取 access_token ,设备码只能用一次,access_token有效期一个月
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = auth_api.AuthApi(api_client)
            code = device_code  # str | device code
          

            try:
                api_response = api_instance.oauth_token_device_token(
                    code, self.client_id, self.client_secret
                )
                pprint(api_response)
                """
                {
                    expires_in: 2592000,
                    refresh_token: "127.e4971f7944a193bf054ec66c091.YHe2H-QUlWRoj7RmX_F-PeKiQtjKKruvkQgBmfY.PtsH-Q",
                    access_token: "126.ee2ca5592d5289eeba126bc98ff.YHmyFbqEz_EUyG0EnsTXREp9VqDJmyIDpxeA1zw.EzfneA",
                    session_secret: "",
                    session_key: "",
                    scope: "basic netdisk"
                }
                """
                return api_response
            except openapi_client.ApiException as e:
                print(
                    "Exception when calling AuthApi->oauth_token_device_token: %s\n" % e
                )

    def refresh_token(self, refresh_token: str):
        url = f"https://openapi.baidu.com/oauth/2.0/token?grant_type=refresh_token&refresh_token={refresh_token}&client_id={self.client_id}&client_secret={self.client_secret}"

        payload = {}
        headers = {"User-Agent": "pan.baidu.com"}

        response = requests.request("GET", url, headers=headers, data=payload)

        result = response.json()
        print(result)
        """
        {
            expires_in: 2592000,
            refresh_token: "127.e4971f7944a154ec66c091.YHe2H-QUlWRoj7RmX_F-PeKiQtjKKruvkQgBmfY.PtsH-Q",
            access_token: "126.ee2ca552885eeba126bc98ff.YHmyFbqEz_EUyGJmyIDpxeA1zw.EzfneA",
            session_secret: "",
            session_key: "",
            scope: "basic netdisk"
        }
        """
        return result
