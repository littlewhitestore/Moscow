# -*- coding:utf-8 -*-

# from lxml import etree
# import urllib


# def getHtml(url):
#     page = urllib.urlopen(url)
#     html = page.read()
#     return html


# if __name__ == '__main__':
#
#     html = getHtml('https://item.taobao.com/item.htm?spm=a219r.lm897.14.6.79f546e2k69e1W&id=15678310222&ns=1&abbucket=12#detail')
#
#     res = etree.HTML(html)
#     # print res
#     data = res.xpath('//*[@id="J_Title"]/h3/text()')\
#     print(data)







# -*- coding:utf-8 -*-

from lxml import etree
import urllib


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


if __name__ == '__main__':

    html = getHtml('https://detail.1688.com/offer/528506897951.html')

    res = etree.HTML(html)
    data = res.xpath('//*[@id="mod-detail-price"]/div/table/tbody/tr[1]/td[2]/span[2]/text()')
    print(data)





