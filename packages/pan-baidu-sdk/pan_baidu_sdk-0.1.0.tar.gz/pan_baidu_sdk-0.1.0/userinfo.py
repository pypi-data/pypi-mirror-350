import openapi_client
from openapi_client.api import userinfo_api
from pprint import pprint


class UserApi:
    def __init__(self, token):
        self.token = token

    def user_quota(self):
        """
        user_quota demo
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = userinfo_api.UserinfoApi(api_client)
            access_token = self.token  # str |
            checkexpire = 1  # int |  (optional)
            checkfree = 1  # int |  (optional)

            try:
                api_response = api_instance.apiquota(
                    access_token, checkexpire=checkexpire, checkfree=checkfree
                )
                print(api_response)
                """
                {
                    "errno": 0,
                    "total": 2205465706496,
                    "free": 2205465706496,
                    "request_id": 4890482559098510375,
                    "expire": false,
                    "used": 686653888910
                }
                """
                return api_response

            except openapi_client.ApiException as e:
                print("Exception when calling UserinfoApi->apiquota: %s\n" % e)

    def user_info(self):
        """
        user_info demo
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = userinfo_api.UserinfoApi(api_client)
            access_token = self.token  # str |

            try:
                api_response = api_instance.xpannasuinfo(access_token)
                pprint(api_response)

                """
                {
                    "avatar_url": "https://dss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/item/netdisk.1.3d20c095.phlucxvny00WCx9W4kLifw.jpg",
                    "baidu_name": "百度用户A001",
                    "errmsg": "succ",
                    "errno": 0,
                    "netdisk_name": "netdiskuser",
                    "request_id": "674030589892501935",
                    "uk": 208281036,
                    "vip_type": 2
                }
                """
                return api_response

            except openapi_client.ApiException as e:
                print("Exception when calling UserinfoApi->xpannasuinfo: %s\n" % e)
