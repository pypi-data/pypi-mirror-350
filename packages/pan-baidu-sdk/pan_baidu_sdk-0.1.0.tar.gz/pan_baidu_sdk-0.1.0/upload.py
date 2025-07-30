import os
from pprint import pprint
from openapi_client.api import fileupload_api
import openapi_client
import hashlib
import json
import tempfile
import shutil


class UploadApi:
    def __init__(self, token: str):
        self.token = token

    def _precreate(self, filesize, filepath, filemd5s):
        """
        precreate
        预上传是通知网盘云端新建一个上传任务,网盘云端返回唯一ID uploadid 来标识此上传任务.
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = fileupload_api.FileuploadApi(api_client)
            access_token = self.token  # str |
            path = filepath  # str | 上传后使用的文件绝对路径,需要urlencode 对于一般的第三方软件应用,路径以 "/apps/your-app-name/" 开头.对于小度等硬件应用,路径一般 "/来自:小度设备/" 开头.对于定制化配置的硬件应用,根据配置情况进行填写.
            isdir = 0  # int | isdir
            size = filesize  # int | size 文件和目录两种情况:上传文件时,表示文件的大小,单位B;上传目录时,表示目录的大小,目录的话大小默认为0
            autoinit = 1  # int | autoinit
            block_list = filemd5s  # str | 由MD5字符串组成的list,文件各分片MD5数组的json串.block_list的含义如下,如果上传的文件小于4MB,其md5值(32位小写)即为block_list字符串数组的唯一元素;如果上传的文件大于4MB,需要将上传的文件按照4MB大小在本地切分成分片,不足4MB的分片自动成为最后一个分片,所有分片的md5值(32位小写)组成的字符串数组即为block_list.
            rtype = 3  # int | rtype (optional)

            try:
                api_response = api_instance.xpanfileprecreate(
                    access_token, path, isdir, size, autoinit, block_list, rtype=rtype
                )
                pprint(api_response)
                return api_response["uploadid"]
            except openapi_client.ApiException as e:
                print(
                    "Exception when calling FileuploadApi->xpanfileprecreate: %s\n" % e
                )

    def _upload_chunk(self, uploadid, filepath, tempfile, seq):
        """
        uploadid    上一个阶段预上传precreate接口下发的uploadid
        upload 如果文件大小小于等于4MB,无需切片,直接上传即可
        文件分两种类型 :
        小文件,是指文件大小小于等于4MB的文件,成功调用一次本接口后,表示分片上传阶段完成.
        大文件,是指文件大小大于4MB的文件,需要先将文件按照4MB大小进行切分,然后针对切分后的分片列表,逐个分片进行上传,分片列表的分片全部成功上传后,表示分片上传阶段完成.
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = fileupload_api.FileuploadApi(api_client)
            access_token = self.token  # str |
            partseq = f"{seq}"  # str | 文件分片的位置序号,从0开始,参考上一个阶段预上传precreate接口返回的block_list
            path = filepath  # str | 远程文件路径
            type = "tmpfile"  # str | 固定值
            try:
                file = open(tempfile, "rb")  # file | 要进行传送的本地文件分片 char[]
            except Exception as e:
                print("Exception when open file: %s\n" % e)
                exit(-1)

            try:
                api_response = api_instance.pcssuperfile2(
                    access_token, partseq, path, uploadid, type, file=file
                )
                pprint(api_response)
            except openapi_client.ApiException as e:
                print("Exception when calling FileuploadApi->pcssuperfile2: %s\n" % e)

    def _create(self, uploadid, filepath, filesize, filemd5s):
        """
        create 将分片合并,创建文件
        uploadid precreate返回的uploadid
        """
        with openapi_client.ApiClient() as api_client:
            api_instance = fileupload_api.FileuploadApi(api_client)
            access_token = self.token  # str |
            path = filepath  # str | 与precreate的path值保持一致
            isdir = 0  # int | isdir
            size = filesize  # int | 与precreate的size值保持一致
            block_list = filemd5s  # str | 与precreate的block_list值保持一致
            rtype = 3  # int | rtype (optional)

            try:
                api_response = api_instance.xpanfilecreate(
                    access_token, path, isdir, size, uploadid, block_list, rtype=rtype
                )
                pprint(api_response)
            except openapi_client.ApiException as e:
                print("Exception when calling FileuploadApi->xpanfilecreate: %s\n" % e)

    def _split_file_into_chunks(self, file_path, chunk_size=4 * 1024 * 1024):
        """
        将文件分片并保存到系统临时目录 同时计算每个分片的MD5值
        :param file_path: 要分割的原始文件路径
        :param chunk_size: 分片大小(字节),默认4MB
        :return: 包含(分片路径,MD5)的列表
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"文件不存在:{file_path}")

        # 创建一个临时目录
        temp_dir = tempfile.mkdtemp()
        base_name = os.path.basename(file_path)
        chunks_info = []
        index = 0

        with open(file_path, "rb") as original_file:
            while True:
                chunk_data = original_file.read(chunk_size)
                if not chunk_data:
                    break

                # 计算MD5
                md5_hash = hashlib.md5(chunk_data).hexdigest()

                # 生成分片文件名
                chunk_filename = os.path.join(temp_dir, f"{base_name}.part{index}")

                # 写入分片文件
                with open(chunk_filename, "wb") as chunk_file:
                    chunk_file.write(chunk_data)

                # 记录分片信息
                chunks_info.append((chunk_filename, md5_hash))
                index += 1

        return chunks_info, temp_dir

    def upload(self, local_file, remote_file):
        if os.path.exists(local_file):  # 检查路径是否存在(文件或目录)
            if os.path.isfile(local_file):  # 明确检查是否为文件
                print("本地文件存在")
            else:
                print(f"本地路径存在,但不是文件:{local_file}")
                return
        else:
            print(f"本地文件不存在:{local_file}")
            return

        filesize = os.path.getsize(local_file)

        filemd5s = []
        tempfiles = []
        temp_dir = None

        try:
            result, temp_dir = self._split_file_into_chunks(local_file)
            print("文件分片完成,各分片信息:")
            for filename, md5 in result:
                print(f"分片文件:{filename}\tMD5:{md5}")
                filemd5s.append(md5)
                tempfiles.append(filename)
        except Exception as e:
            print(f"处理失败:{str(e)}")
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return

        md5str = json.dumps(filemd5s)
        print(md5str)  # 输出: ["a","b","c"]

        uploadid = self._precreate(filesize, remote_file, md5str)

        try:
            for index, item in enumerate(tempfiles):
                self._upload_chunk(uploadid, remote_file, item, index)

            self._create(uploadid, remote_file, filesize, md5str)
        except Exception as e:
            print(f"上传失败:{str(e)}")
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
