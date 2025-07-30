from pan_baidu_sdk.upload import UploadApi
from pan_baidu_sdk.file import FileApi
from pprint import pprint
import json
import time
from pan_baidu_sdk.download import DownloadApi
from pan_baidu_sdk.user import UserApi

def main():
    # 读取 token，从 ~/.baidu_webdisk/config.json 中读取

    token = ""
    with open("/Users/yinnan/.baidu_webdisk/config.json", "r") as f:
        config = json.load(f)
        # 读取 token
        token = config["access_token"]
        print(token)

    # 创建文件夹
    file_api = FileApi(token)
    mkdir_res1 = file_api.mkdir("/文件夹测试/相册1")
    pprint(f"创建文件夹：{mkdir_res1}")
    mkdir_res2 = file_api.mkdir("/文件夹测试/相册2")
    pprint(f"创建文件夹：{mkdir_res2}")
    time.sleep(1)

    # 上传文件
    upload_api = UploadApi(token)
    upload_res = upload_api.upload(
        "/Users/yinnan/Pictures/wallpaper/wallpaper.jpg",
        "/文件夹测试/相册1/wallpaper.jpg",
    )
    pprint(f"上传结果：{upload_res}")
    time.sleep(1)

    # 列出文件
    files = file_api.list("/文件夹测试/相册1")
    if files is None:
        pprint("列出文件失败")
        return

    pprint(files)
    time.sleep(1)

    # 下载文件
    fsid = files[0]["fs_id"]
    pprint(fsid)

    down_api = DownloadApi(token)
    down_api.download(fsid, "/Users/yinnan/yin-data/temp")
    metas = file_api.file_info(fsid)
    pprint("文件元数据：")
    pprint(metas)

    time.sleep(1)
    # 移动文件
    move_res = file_api.move(
        "/文件夹测试/相册1/wallpaper.jpg", "/文件夹测试/相册2", "wallpaper.jpg"
    )
    pprint(f"文件移动：{move_res}")
    time.sleep(1)

    # 重命名文件
    rename_res = file_api.rename("/文件夹测试/相册2/wallpaper.jpg", "new_wallpaper.jpg")
    pprint(f"重命名：{rename_res}")
    time.sleep(1)

    # 删除文件
    delete_res1 = file_api.delete("/文件夹测试/相册1")
    pprint(f"删除：{delete_res1}")

    delete_res2 = file_api.delete("/文件夹测试/相册2")
    pprint(f"删除：{delete_res2}")

    # 获取文件信息
    # 获取用户信息
    user_api = UserApi(token)
    pprint(user_api.user_info())
    pprint(user_api.user_quota())

if __name__ == "__main__":
    main()
