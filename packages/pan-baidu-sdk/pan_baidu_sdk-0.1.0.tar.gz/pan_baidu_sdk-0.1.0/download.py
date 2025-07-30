import requests
from listfile import ListFileApi
import os


class DownloadApi:
    def __init__(self, token: str):
        self.token = token
        self.list_file_api = ListFileApi(self.token)

    def _download_file(self, url: str, filename: str) -> str:
        """
        下载文件
        """

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

    def download(self, fsid, dest_dir) -> str:
        result = self.list_file_api.filemetas(fsid)
        dest_filepath = os.path.join(dest_dir, f"{result['filename']}")
        saved_path = self._download_file(
            result["dlink"] + f"&access_token={self.token}", dest_filepath
        )
        print(f"文件已保存到:{saved_path}")
        return result["path"]
