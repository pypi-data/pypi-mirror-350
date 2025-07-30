import requests
from .file import FileApi
import os


class DownloadApi:
    def __init__(self, token: str):
        self.token = token
        self.file_api = FileApi(self.token)

    def _download_file(self, url: str, filename: str) -> str:
        """
        下载文件
        """
        try:
            headers = {
                "User-Agent": "pan.baidu.com",  # 伪装成百度网盘客户端
                "Referer": "https://pan.baidu.com/",  # 可选:添加来源页
            }
            # 发送 HTTP 请求(开启流式传输节省内存)
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()  # 自动处理 4xx/5xx 错误

            # 流式写入文件
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # 过滤保活数据块
                        f.write(chunk)

            return str(filename)
        except requests.RequestException as e:
            raise Exception(f"下载文件时发生网络错误: {str(e)}")
        except IOError as e:
            raise Exception(f"保存文件时发生IO错误: {str(e)}")
        except Exception as e:
            raise Exception(f"下载文件时发生未知错误: {str(e)}")

    def download(self, fsid, dest_dir) -> bool:
        try:
            result = self.file_api.file_info(fsid)
            dest_filepath = os.path.join(dest_dir, f"{result['filename']}")
            saved_path = self._download_file(
                result["dlink"] + f"&access_token={self.token}", dest_filepath
            )
            print(f"文件已保存到:{saved_path}")
            return True
        except Exception as e:
            print(e)
            return False
