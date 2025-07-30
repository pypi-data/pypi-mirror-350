from pprint import pprint
import openapi_client
from openapi_client.api import filemanager_api
import json
import requests


class FileOperationApi:
    def __init__(self, token):
        self.token = token

    def move(self, filepath: str, destdir: str, newname: str):
        """
        filemanager move
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = filemanager_api.FilemanagerApi(api_client)
            access_token = self.token  # str |
            _async = 1  # int | async
            filelist_obj = {"path": filepath, "dest": destdir, "newname": newname}

            filelist = f"[{json.dumps(filelist_obj)}]"
            ondup = "fail"  # str | ondup (optional)

            try:
                api_response = api_instance.filemanagermove(
                    access_token, _async, filelist, ondup=ondup
                )
                print(api_response)
            except openapi_client.ApiException as e:
                print(
                    "Exception when calling FilemanagerApi->filemanagermove: %s\n" % e
                )

    def rename(self, filepath: str, newname: str):
        """
        filemanager rename
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = filemanager_api.FilemanagerApi(api_client)
            access_token = self.token  # str |
            _async = 1  # int | async
            filelist_obj = {"path": filepath, "newname": newname}
            filelist = f"[{json.dumps(filelist_obj)}]"  # str | filelist
            ondup = "fail"  # str | ondup (optional)

            try:
                api_response = api_instance.filemanagerrename(
                    access_token, _async, filelist, ondup=ondup
                )
                pprint(api_response)
            except openapi_client.ApiException as e:
                print(
                    "Exception when calling FilemanagerApi->filemanagerrename: %s\n" % e
                )

    def delete(self, filepath):
        """
        filemanager delete 删除文件或目录
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = filemanager_api.FilemanagerApi(api_client)
            access_token = self.token  # str |
            _async = 1  # int | async
            filelist_obj = {"path": filepath}

            filelist = f"[{json.dumps(filelist_obj)}]"  # str | filelist
            ondup = "fail"  # str | ondup (optional)

            try:
                api_response = api_instance.filemanagerdelete(
                    access_token, _async, filelist, ondup=ondup
                )
                print(api_response)
            except openapi_client.ApiException as e:
                print(
                    "Exception when calling FilemanagerApi->filemanagerdelete: %s\n" % e
                )

    def mkdir(self, dir_name):
        """
        创建文件夹，绝对路径
        """
        url = f"https://pan.baidu.com/rest/2.0/xpan/file?method=create&access_token={self.token}"

        payload = {
            "path": dir_name,
            "rtype": "0",  # 文件命名策略，默认0, 0 为不重命名，返回冲突, 1 为只要path冲突即重命名
            "isdir": "1",  # 创建文件夹的绝对路径，需要urlencode
        }
        files = []
        headers = {}

        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files
        )

        print(response.text.encode("utf8"))
