# -*- coding: utf-8 -*-
import codecs
import json

class AutopjtPipeline(object):
    
    def __init__(self):
        self.file = codecs.open("/home/python/getdata.json", "wb", encoding="utf-8")
    
    def process_item(self, item, spider):
        
        for j in range(0,len(item["name"])):
            #将当前页的第j个商品的名称赋值给变量name
            name=item["name"][j]
            price=item["price"][j]
            comnum=item["comnum"][j]
            link=item["link"][j]
            
            #将当前页下第j个商品的name、price、comnum、link等信息处理一下
            #重新组合成一个字典
            books={"name":name,"price":price,"comnum":comnum,"link":link}
            
            #将组合后的当前页中第j个商品的数据写入json文件
            i=json.dumps(dict(books), ensure_ascii=False)
            line = i + '\n'
            self.file.write(line)
        return item
    
    def close_spider(self,spider):
        self.file.close()
