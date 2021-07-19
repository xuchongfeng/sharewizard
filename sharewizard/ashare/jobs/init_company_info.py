#!/usr/bin/python
# coding: utf-8

from service.tu_share import TuShare

import sys
import os
import django

# 获取当前文件的目录
pwd = os.path.dirname(os.path.realpath(__file__))
# 获取项目名的目录(因为我的当前文件是在项目名下的文件夹下的文件.所以是../)
sys.path.append(pwd + "../../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sharewizard.settings")

django.setup()

from ashare.models import Company

TOKEN = "53d33fa381e94af6cd8e5b5165d5802ad40dd92a5094a6dd175d2a89"


def work():
    tu_share = TuShare(TOKEN)
    stock_list = tu_share.get_stock_basic_info()
    for stock in stock_list:
        company = Company(name=stock[2], code=stock[0], industry=stock[3])
        company.save()


def init_url():
    companys = Company.objects.all()
    for company in companys:
        code = company.code
        company.url = "https://xueqiu.com/S/" + code.split(".")[1] + code.split(".")[0]
        company.save()


if __name__ == "__main__":
    # work()
    init_url()
