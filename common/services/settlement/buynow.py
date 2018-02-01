# *-* coding:utf-8 *-*

class CheckItem(object):
    def __init__(self, sku, number):
        self.sku = sku
        self.number = number

class CheckList(object):
    '''
    结算清单
    '''

    def __init__(self):
        self.sku_list = []
        self.total_amount = 0           #商品金额
        self.postage = 0                #运费
        self.is_free_postage = True     #是否包邮
        self.amount_payable = 0         #应付金额
        self.receiver = None

    def check_sku(self, sku, number):
        self.sku_list.append(CheckItem(sku, number))
        self.total_amount += sku.price * number

class BuyNowSettlementService(object):
    def __init__(self, sku, number, receiver=None):
        self.sku = sku
        self.number = number
        self.receiver = receiver

        self.check_list = CheckList()

    def settlement(self):
        self.__calc_total_amount()
        self.__calc_postage()
        return self.check_list

    def __calc_total_amount(self):
        self.check_list.check_sku(self.sku, self.number)
        self.check_list.amount_payable = self.check_list.total_amount

    def __is_free_postage(self):
        return True

    def __calc_postage(self):
        self.check_list.receiver = self.receiver
        is_free_postage = self.__is_free_postage()
        self.check_list.is_free_postage = is_free_postage
        if is_free_postage is True:
            self.check_list.postage = 0
        else:
            self.check_list.postage = 0
