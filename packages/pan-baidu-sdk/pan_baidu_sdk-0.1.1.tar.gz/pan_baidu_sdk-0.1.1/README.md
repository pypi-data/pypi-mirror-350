# 百度网盘 SDK

这是一个用于操作百度网盘的 Python SDK，提供了文件上传、下载、列表等功能。

## 安装

```bash
pip install pan-baidu-sdk
```

## 使用方法

```python
from pan_baidu_sdk import BaiduPan

# 初始化客户端
client = BaiduPan()

# 上传文件
client.upload_file("本地文件路径", "网盘目标路径")

# 下载文件
client.download_file("网盘文件路径", "本地保存路径")

# 获取文件列表
files = client.list_files("网盘目录路径")
```

## 功能特性

- 文件上传
- 文件下载
- 文件列表
- 用户信息查询

## 依赖要求

- Python >= 3.12
- requests >= 2.32.3

## 许可证

MIT License
