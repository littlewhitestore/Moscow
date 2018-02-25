# coding=utf-8
import re
import uuid
import requests
import ntpath
import mimetypes
import hashlib
import sys
import logging
from tempfile import NamedTemporaryFile

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


class ImageStorage(object):
    BUCKET_SIZE = 16
    BUCKET_FORMAT = "img-prod-{:0>3d}-1255633922"
    QCLOUD_CONFIG = {
        'secret_id': 'AKIDjOTO9qnlxyoBe2aJB2vmTzKVYVL5m6NT',
        'secret_key': '65t0xlYEnCQn2771nR3Ys18A2oT3Yy31',
        'region': 'ap-beijing',
    }

    @staticmethod
    def upload_from_url(url):
        try:
            filename = re.findall('.*/(\S+)\??', url)[0]
            prefix=filename.split('.')[0]
            suffix=filename.split('.')[1] 
        except Exception, e:
            filename = str(uuid.uuid4())
            prefix=filename
            suffix=None

        f = NamedTemporaryFile(delete=True, suffix=suffix, prefix=prefix)
        res = requests.get(url)
        f.write(res.content)
        f.seek(0)

        download_filename = f.name
        url = ImageStorage.upload_from_file(download_filename)
        f.close()
        return url

    @staticmethod
    def upload_from_file(filename):
        con = open(filename, 'r').read() 
        key = ntpath.basename(filename)
        return ImageStorage.upload_from_stream(con, filename)

    @staticmethod
    def upload_from_stream(stream, filename):
        DEFAULT_MIME_TYPE = "application/octet-stream"
        try:
            mimetypes.init()
            content_type = mimetypes.types_map.get(".%s"%filename.split('.')[-1], DEFAULT_MIME_TYPE)
        except Exception, e:
            content_type = DEFAULT_MIME_TYPE

        object_key = ImageStorage.generate_stream_key(stream)
        bucket = ImageStorage.get_bucket_by_key(object_key)

        config = CosConfig(
            Region=ImageStorage.QCLOUD_CONFIG['region'], 
            Secret_id=ImageStorage.QCLOUD_CONFIG['secret_id'], 
            Secret_key=ImageStorage.QCLOUD_CONFIG['secret_key'], 
            Token=''
        )
        upload_client = CosS3Client(config)
        #TODO setting content-type
        response = upload_client.put_object(
            Bucket=bucket,
            Body=stream,
            Key=object_key,
            Metadata={
                'x-cos-acl': "public-read",
            }
        )
        if response:
            return object_key
        else:
            raise Exception('UPLOAD INTO CLOUD ERROR')

    @staticmethod
    def generate_stream_key(stream):
        sig = hashlib.md5()
        sig.update(stream)
        key = sig.hexdigest()
        return key
    
    @staticmethod
    def get_bucket_by_key(key):
        prefix = int(key[:1], ImageStorage.BUCKET_SIZE)
        bucket = ImageStorage.BUCKET_FORMAT.format(prefix)
        return bucket

    @staticmethod
    def get_url_by_key(key):
        bucket = ImageStorage.get_bucket_by_key(key)
        PUBLIC_READ_URL = "http://{bucket}.cos.{region}.myqcloud.com/{key}"
        url = PUBLIC_READ_URL.format(bucket=bucket, region=ImageStorage.QCLOUD_CONFIG['region'], key=key)
        return url 

        

if __name__ == "__main__":
    urls = [
        "https://www.microsoft.com/zh-hk/CMSImages/WindowsHello_Poster_1920-1600x300-hello.png?version=0d8f51c7-ef87-b0af-8f26-453fb40b4b7d",
        "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1519547364079&di=b1a7381c8478b739d75aa52b5f394063&imgtype=0&src=http%3A%2F%2Fimg.pconline.com.cn%2Fimages%2Fupload%2Fupc%2Ftx%2Fwallpaper%2F1207%2F16%2Fc0%2F12347883_1342409469170.jpg"
    ]
    def upload(url):
        key = ImageStorage.upload_from_url(url)
        new_url = ImageStorage.get_url_by_key(key)
        assert new_url
        assert url != new_url
        assert "myqcloud.com" in new_url
        return new_url

    new_urls = set()
    for url in urls:
        new_url = upload(url)
        print new_url
        new_urls.add(new_url)
    assert len(new_urls) == len(urls)
