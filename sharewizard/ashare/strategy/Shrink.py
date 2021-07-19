#!/usr/bin/python
# coding: utf-8

"""
策略说明:
    收缩模型：识别股票在一段拉伸之后的筑底回落，等待二次上涨
    特征：
       - N天内，价格的走势为先升，后降，逐渐趋于平稳，平稳的天数在M天内
         - 最高点，在前半段，最低点在后半段
         - 平稳的意思是指，价格相差S个点以内
       - N天内，价格最高点和最低点，相差在E-F个点
       - 交易量的走势：先上升，后平稳下降，以P天平均交易量为一个单位, 交易量是下降，趋于平稳的。
         计算规则：最高交易量和最低交易量相差Q%，交易量降低的次数占X%
目标：
    筛选出来的股票，应该在一周之内开启上涨通道
"""


class Shrink(object):
    def __init__(self, days=30,
                 stable_days=4,
                 stable_gap_percentage=10,
                 price_gap_low=10,
                 price_gap_high=20,
                 cell_days=2,
                 trade_amount_gap_low_percentage=15,
                 trade_amount_gap_high_percentage=30,
                 trade_amount_reduce_low_percentage=20):
        self.days = days
        self.stable_days = stable_days
        self.stable_gap_percentage = stable_gap_percentage
        self.price_gap_low = price_gap_low
        self.price_gap_high = price_gap_high
        self.cell_days = cell_days
        self.trade_amount_gap_low_percentage = trade_amount_gap_low_percentage
        self.trade_amount_gap_high_percentage = trade_amount_gap_high_percentage
        self.trade_amount_reduce_low_percentage = trade_amount_reduce_low_percentage

    def filter(self, price_amount_list):
        """
        :param 价格与交易量列表：[(price, amount)]
        :return:
        """
        # rule-1: 价格的走势为先升后降
        if len(price_amount_list) == 0:
            return False

        price_list = [price_amount[0] for price_amount in price_amount_list]
        amount_list = [float(price_amount[1]) for price_amount in price_amount_list]

        max_price = max(price_list)
        low_price = min(price_list)

        max_price_idx = price_list.index(max_price)
        low_price_idx = price_list.index(low_price)

        if max_price_idx > low_price_idx:
            return False

        # rule-2: 最近M天的价格波动在M%以内
        max_stable_price = max(price_list[:self.stable_days])
        min_stable_price = min(price_list[:self.stable_days])

        if (max_stable_price-min_stable_price) / max_stable_price * 100 > \
                self.stable_gap_percentage:
            return False

        # rule-3: 最高点和最低点相差E-F个点
        gap_percentage = (max_price - low_price) / max_price
        if gap_percentage > self.trade_amount_gap_high_percentage:
            return False

        # rule-4: 交易量先上升，后面趋于平稳
        n_day_amount_list = []
        for i in range(0, len(amount_list) - self.cell_days):
            n_day_amount_list.append(sum(amount_list[i:i+self.cell_days]))

        # rule-4-1: 交易量上升
        max_amount = max(n_day_amount_list)
        max_amount_idx = n_day_amount_list.index(max_amount)
        min_amount = min(n_day_amount_list)
        min_amount_idx = n_day_amount_list.index(min_amount)

        if max_amount_idx > min_amount_idx:
            return False

        # rule-4-2: 交易量平稳，并降低到最高值的一定比例
        if (((max_amount - min_amount) * 100) / max_amount) < self.trade_amount_reduce_low_percentage:
            return False

        return True