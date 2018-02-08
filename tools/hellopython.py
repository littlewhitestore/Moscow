# coding=utf-8


import os
import requests
import re
import csv
import codecs

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError



class fileObj(object):
    def __init__(self):
        self.tb_id = ""
        self.goods_name =""
        self.goods_price =""
        self.banner_url = []
        self.desc_img_url = []
        self.desc_string = []
        self.stock = 1000

def req_qclooud():
    print "=================进入req方法"
    # 设置用户属性, 包括secret_id, secret_key, region
    # appid已在配置中移除,请在参数Bucket中带上appid。Bucket由bucketname-appid组成
    secret_id = 'AKIDjOTO9qnlxyoBe2aJB2vmTzKVYVL5m6NT'     # 替换为用户的secret_id
    secret_key = '65t0xlYEnCQn2771nR3Ys18A2oT3Yy31'     # 替换为用户的secret_key
    region = 'ap-guangzhou'    # 替换为用户的region
    token = ''                 # 使用临时秘钥需要传入Token，默认为空,可不填
    config = CosConfig(Region=region, Secret_id=secret_id, Secret_key=secret_key, Token=token)  #获取配置对象
    client = CosS3Client(config)                                                                #获取客户端对象
    # 文件流 简单上传
    dir_path = '/Users/e/xiaobaike/xiaobai_data'
    for file in os.listdir(dir_path):
        if (not os.path.isdir(os.path.join(dir_path,file))) and is_img(os.path.splitext(file)[1]):
            with open(os.path.join(dir_path,file)) as fp:
                try:
                    response = client.put_object(
                        Bucket='xiaobaidian-img-001-1255633922',
                        Body=fp,
                        Key=file,
                        StorageClass='STANDARD',
                        CacheControl='no-cache',
                        ContentDisposition=file
                        )
                    if(response):
                        print(str(os.listdir(dir_path).index(file))+"/"+str(len(os.listdir(dir_path))-1))
                        print("图片"+file+"==上传成功")
                        
                except Exception, e  :
                    print(str(os.listdir(dir_path).index(file))+"上传失败")
                    prn_obj(e)
        else :
            print(str(os.listdir(dir_path).index(file))+"="+file +"是非图片文件或者文件夹")
    print ('文件上传任务执行结束')

#判断文件名是否是图片后缀
def is_img(ext):
    ext = ext.lower()
    if ext == '.jpg':
        return True
    elif ext == '.png':
        return True
    elif ext == '.jpeg':
        return True
    elif ext == '.bmp':
        return True
    else:
        return False

def readCsvToData():
# 读取csv文件方式1
    global file_csv_path
    global goods_banner_dir
    print "读取csv 路径= " + file_csv_path
    with open(file_csv_path, "r") as csvFile:
        reader = csv.DictReader(csvFile.read().splitlines(), delimiter='\t' )  # 返回的是迭代类型
        col_title = [row for row in reader]
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~"
        for item in col_title:
            print type(item)
            print len(item)
            print item.keys() 
            file_obj = fileObj()
            file_obj.goods_name = item['title']
            file_obj.goods_price = item['price']
            file_obj.tb_id =item['num_id']

            desc_string = item['description']
            img_string = item['picture']
            for pic_str_c in img_string.split('|;'):
                banner_img = goods_banner_dir + pic_str_c.split(':')[0]                          
                file_obj.banner_url.append(banner_img)
            prn_obj(file_obj)
    csvFile.close()
    data = []
    return data

#解析csv文件内容
def parseCsv():
    print "1" 
def prn_obj(obj): 
    print '\n'.join(['%s:%s' % item for item in obj.__dict__.items()]) 
if __name__ == '__main__':
    req_qclooud()
