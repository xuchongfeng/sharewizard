#!/usr/bin/python
# coding: utf-8

import datetime


def today():
    return datetime.date.today()


def get_n_days_ago(m):
    today = datetime.date.today()
    s_m_date = datetime.timedelta(days=m)
    return today - s_m_date