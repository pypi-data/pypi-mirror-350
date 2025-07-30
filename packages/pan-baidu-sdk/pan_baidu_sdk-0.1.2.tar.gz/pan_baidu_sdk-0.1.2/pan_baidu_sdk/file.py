from pprint import pprint
from openapi_client.api import multimediafile_api
from openapi_client.api import fileinfo_api
from .utils import process_path
import openapi_client
from openapi_client.api import filemanager_api
import json
import requests


class FileApi:
    def __init__(self, token):
        self.token = token

    def list(self, remote_path, start=0, limit=1000):
        """
        listall 列出目录中所有的文件和目录
        """
        self.remote_path_ab = process_path(remote_path)
        with openapi_client.ApiClient() as api_client:
            api_instance = multimediafile_api.MultimediafileApi(api_client)
            access_token = self.token  # str |
            path = self.remote_path_ab  # str |
            recursion = 0  # int | 是否递归获取子目录
            web = "1"  # str |  (optional)

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
                return api_response["list"]
            except openapi_client.ApiException as e:
                print(
                    "Exception when calling MultimediafileApi->xpanfilelistall: %s\n"
                    % e
                )

    def file_info(self, fsid):
        """
        filemetas 文件详情
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

                fileitem = api_response["list"][0]

                """
                {
                    'category': 3,
                    'dlink': 'https://d.pcs.baidu.com/file/1519a56c3r286be40de53eb11f6f7c19?fid=897597305-250528-275427756253768&rt=pr&sign=FDtAERK-DCb740ccc5511e5e8fedcff06b081203-N0WC4RHbfsjd1NYs7Lgn6UjbboM%3D&expires=8h&chkbd=0&chkv=0&dp-logid=2457833243742112623&dp-callid=0&dstime=1748333958&r=645106218&vuk=897597305&origin_appid=26430790&file_type=0',
                    'duration': 0,
                    'filename': 'wallpaper.jpg',
                    'fs_id': 275427756253768,
                    'isdir': 0,
                    'local_ctime': 1748333953,
                    'local_mtime': 1748333953,
                    'md5': '1519a56c3r286be40de53eb11f6f7c19',
                    'oper_id': 897597305,
                    'path': '/apps/Webdisk/文件夹测试/相册1/wallpaper.jpg',
                    'server_ctime': 1748333953,
                    'server_mtime': 1748333953,
                    'size': 2965976,
                    'thumbs': {
                                'icon': 'https://thumbgn=FDTA597305&ft=image',
                                'url1': 'https://thcs.com/thumbnail/&time=1748332800&size=c140_u90&quality=100&vuk=897597305&ft=image',
                                'url2': 'https://thcs.com/thumbnail/&time=1748332800&size=c360_u270&quality=100&vuk=897597305&ft=image',
                                'url3': 'https://thcs.com/thumbnail/&time=1748332800&size=c850_u580&quality=100&vuk=897597305&ft=image',
                                'url4': 'https://thcs.com/thumbnail/&time=1748332800&size=c165_u165&quality=100&vuk=897597305&ft=image'
                            }
                }
                                    
                """

                return fileitem

            except openapi_client.ApiException as e:
                print(
                    "Exception when calling MultimediafileApi->xpanmultimediafilemetas: %s\n"
                    % e
                )

    def search(self, keyword: str):
        """
        search 在根目录中搜索文件
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
                return api_response
            except openapi_client.ApiException as e:
                print("Exception when calling FileinfoApi->xpanfilesearch: %s\n" % e)

    def move(self, filepath: str, destdir: str, newname: str):
        """
        move 移动文件到指定目录，可选择重命名文件
        """
        
        filepath_ab = process_path(filepath)
        destdir_ab = process_path(destdir)

        with openapi_client.ApiClient() as api_client:
            api_instance = filemanager_api.FilemanagerApi(api_client)
            access_token = self.token  # str |
            _async = 1  # int | async
            filelist_obj = {
                "path": filepath_ab,
                "dest": destdir_ab,
                "newname": newname,
            }

            filelist = f"[{json.dumps(filelist_obj)}]"
            ondup = "fail"  # str | ondup (optional)

            try:
                api_response = api_instance.filemanagermove(
                    access_token, _async, filelist, ondup=ondup
                )
                """
                {
                    "errno": 0,
                    "info": [
                        {
                            "errno": 0,
                            "path": "/apps/Webdisk/文件夹测试/相册2"
                        }
                    ],
                    "request_id": 9166295937311257156
                }
                """
                return api_response
            except openapi_client.ApiException as e:
                print(
                    "Exception when calling FilemanagerApi->filemanagermove: %s\n" % e
                )

    def rename(self, curr_path: str, new_path: str):
        """
        rename 重命名文件或文件夹
        命名冲突返回失败
        """
        filepath_ab = process_path(curr_path)
        with openapi_client.ApiClient() as api_client:
            api_instance = filemanager_api.FilemanagerApi(api_client)
            access_token = self.token  # str |
            _async = 1  # int | async
            filelist_obj = {"path": filepath_ab, "newname": new_path}
            filelist = f"[{json.dumps(filelist_obj)}]"  # str | filelist
            ondup = "fail"  # str | ondup (optional)

            try:
                api_response = api_instance.filemanagerrename(
                    access_token, _async, filelist, ondup=ondup
                )
                """
                {
                    "errno": 0,
                    "info": [
                        {
                            "errno": 0,
                            "path": "/apps/Webdisk/文件夹测试/相册2"
                        }
                    ],
                    "request_id": 9166295937311257156
                }
                """
                return api_response
            except openapi_client.ApiException as e:
                print(
                    "Exception when calling FilemanagerApi->filemanagerrename: %s\n" % e
                )

    def delete(self, filepath:str):
        """
        delete 删除文件或目录

        params: 
            filepath 文件或目录路径
        """

        filepath_ab = process_path(filepath)

        with openapi_client.ApiClient() as api_client:
            api_instance = filemanager_api.FilemanagerApi(api_client)
            access_token = self.token  # str |
            _async = 1  # int | async
            filelist_obj = {"path": filepath_ab}

            filelist = f"[{json.dumps(filelist_obj)}]"  # str | filelist
            ondup = "fail"  # str | ondup (optional)

            try:
                api_response = api_instance.filemanagerdelete(
                    access_token, _async, filelist, ondup=ondup
                )
                """
                {
                    "errno": 0,
                    "info": [
                        {
                            "errno": 0,
                            "path": "/apps/Webdisk/文件夹测试/相册2"
                        }
                    ],
                    "request_id": 9166295937311257156
                }
                """
                return api_response
            except openapi_client.ApiException as e:
                print(
                    "Exception when calling FilemanagerApi->filemanagerdelete: %s\n" % e
                )

    def mkdir(self, dir_name) -> bool:
        """
        创建文件夹，可创建多层文件夹
        """
        try:
            url = f"https://pan.baidu.com/rest/2.0/xpan/file?method=create&access_token={self.token}"
            dir_name_ab = process_path(dir_name)
            payload = {
                "path": dir_name_ab,
                "rtype": "0",  # 文件命名策略，默认0, 0 为不重命名，返回冲突, 1 为只要path冲突即重命名
                "isdir": "1",  # 创建文件夹的绝对路径，需要urlencode
            }
            files = []
            headers = {}

            response = requests.request(
                "POST", url, headers=headers, data=payload, files=files
            )
            response.raise_for_status()  # 检查HTTP响应状态
            return True
        except requests.RequestException as e:
            pprint(f"创建文件夹时发生网络错误: {str(e)}")
            return False
        except Exception as e:
            pprint(f"创建文件夹时发生未知错误: {str(e)}")
            return False
