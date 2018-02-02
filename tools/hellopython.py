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
        self.stock = 0
global file_csv_path 
global file_csv_modify_path
file_csv_modify_path = "/Users/e/xiaobaike/xiaobaike_data/商品信息 0201.xlsx"
global goods_banner_dir 
global goods_desc_dir 

def req_qclooud():
    # 设置用户属性, 包括secret_id, secret_key, region
    # appid已在配置中移除,请在参数Bucket中带上appid。Bucket由bucketname-appid组成
    secret_id = 'AKIDjOTO9qnlxyoBe2aJB2vmTzKVYVL5m6NT'     # 替换为用户的secret_id
    secret_key = '65t0xlYEnCQn2771nR3Ys18A2oT3Yy31'     # 替换为用户的secret_key
    region = 'ap-guangzhou'    # 替换为用户的region
    token = ''                 # 使用临时秘钥需要传入Token，默认为空,可不填
    config = CosConfig(Region=region, Secret_id=secret_id, Secret_key=secret_key, Token=token)  #获取配置对象
    client = CosS3Client(config)                                                                #获取客户端对象


    ############################################################################
    # 文件操作                                                                 #
    ############################################################################
    # 1. 上传单个文件
    response = client.put_object(
            Bucket='xiaobaidian-img-001-1255633922',  # Bucket由bucketname-appid组成
            Body='TY'*1024*512*file_size,
            Key=file_name,
            CacheControl='no-cache',
            ContentDisposition='download.txt'
    )

    # 文件流 简单上传
    file_name = 'test.txt'
    with open('test.txt', 'rb') as fp:
        response = client.put_object(
            Bucket='test04-123456789',  # Bucket由bucketname-appid组成
            Body=fp,
            Key=file_name,
            StorageClass='STANDARD',
            CacheControl='no-cache',
            ContentDisposition='download.txt'
    )
    print response['ETag']

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

def getFile():
    file_path = "/Users/e/xiaobaike/xiaobaike_data"
    root_files = os.walk(file_path)
    global file_csv_path
    global goods_banner_dir
    global goods_desc_dir
    
    i = 0
    first_dir = 0
    
    for roots,dirs,files in root_files:
        i+=1
        dir_lv = roots.count("/")
        if i==1:
            first_dir = dir_lv
            print "进入第一层文件循环"
            #第一级目前 包含 cvs与图片初级目录
            for csv_file in files:
                print "遍历files= %s" % csv_file
                if not csv_file.startswith('.'):
                    file_csv_path = roots +"/" +csv_file
                    print "file_csv_path结果 ====%s" %  file_csv_path

        elif (dir_lv - first_dir ==1) :
            #第二级目录 包含 contentPic文件夹 .tbi图片
            goods_banner_dir = roots
            print goods_banner_dir

        elif (dir_lv - first_dir ==2) :
            #第二级目录 包含 一个商品名称的目录
            goods_desc_dir = roots
            print goods_desc_dir
# elif (dir_lv - first_dir ==3) :
            #第三级目录 包含 商品详情的图文文件 
            
        print "减掉后的层次==%s" %(dir_lv - first_dir)
def readCsvToData():
# 读取csv文件方式1
    global file_csv_path
    print "读取csv 路径= " + file_csv_path
    with codecs.open(file_csv_path, "r") as csvFile:
        reader = csv.DictReader(csvFile)  # 返回的是迭代类型
        col_title = [row for row in reader]
#        print "测试循环row === %s" %  col_title
#        col_price = [row['price'] for row in reader]
#        col_desc = [row['description'] for row in reader]
#        col_pic = [row['picture'] for row in reader]
#        col_numid = [row['num_id'] for row in reader]
#        col_subt = [row['subtitle'] for row in reader]
        for item in col_title:
            print "item = %s " %item
#    print "price= %s" % col_price
#    print "desc= %s" % col_desc
#    print "pic= %s" % col_pic
#    print "numid= %s" % col_numid
    csvFile.close()
    data = []
    return data

#解析csv文件内容
def parseCsv():
    print "1" 

if __name__ == '__main__':
    getFile()
    print readCsvToData()
