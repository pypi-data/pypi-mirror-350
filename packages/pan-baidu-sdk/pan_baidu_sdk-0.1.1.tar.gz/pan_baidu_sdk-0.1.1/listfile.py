from pprint import pprint
from openapi_client.api import multimediafile_api
import openapi_client
from openapi_client.api import fileinfo_api


class ListFileApi:
    def __init__(self, token):
        self.token = token

    def listall(self, remote_path):
        """
        listall
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = multimediafile_api.MultimediafileApi(api_client)
            access_token = self.token  # str |
            path = remote_path  # str |
            recursion = 0  # int | 是否递归获取子目录
            web = "1"  # str |  (optional)
            start = 0  # int |  (optional)
            limit = 1000  # int |  (optional)
            order = "time"  # str |  (optional)
            desc = 1  # int |  (optional)

            try:
                api_response = api_instance.xpanfilelistall(
                    access_token,
                    path,
                    recursion,
                    web=web,
                    start=start,
                    limit=limit,
                    order=order,
                    desc=desc,
                )
                pprint(api_response)
                return api_response
            except openapi_client.ApiException as e:
                print(
                    "Exception when calling MultimediafileApi->xpanfilelistall: %s\n"
                    % e
                )

    def filemetas(self, fsid):
        """
        filemetas
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = multimediafile_api.MultimediafileApi(api_client)
            access_token = self.token  # str |
            fsids = f"[{fsid}]"  # str |
            thumb = "1"  # str |  (optional)
            extra = "1"  # str |  (optional)
            dlink = "1"  # str |  (optional)
            needmedia = 1  # int |  (optional)

            try:
                api_response = api_instance.xpanmultimediafilemetas(
                    access_token,
                    fsids,
                    thumb=thumb,
                    extra=extra,
                    dlink=dlink,
                    needmedia=needmedia,
                )
                pprint(api_response)
                fileitem = api_response["list"][0]
               
                return fileitem

            except openapi_client.ApiException as e:
                print(
                    "Exception when calling MultimediafileApi->xpanmultimediafilemetas: %s\n"
                    % e
                )

    def search(self, keyword: str):
        """
        search
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = fileinfo_api.FileinfoApi(api_client)
            access_token = self.token  # str |
            key = keyword  # str |
            web = "1"  # str |  (optional)
            num = "500"  # str |  (optional)
            page = "1"  # str |  (optional)
            dir = "/apps/WebDisk"  # str |  (optional)
            recursion = "1"  # str |  (optional)

            try:
                api_response = api_instance.xpanfilesearch(
                    access_token,
                    key,
                    web=web,
                    num=num,
                    page=page,
                    dir=dir,
                    recursion=recursion,
                )
                pprint(api_response)
            except openapi_client.ApiException as e:
                print("Exception when calling FileinfoApi->xpanfilesearch: %s\n" % e)
