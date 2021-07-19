class NDayHigh(object):
    def _is_n_day_high(self, day_price_list, n, percentage=1):
        day_price_list = day_price_list[:n]
        if len(day_price_list) != 0:
            max_price = max(day_price_list)
            return day_price_list[0][0] >= max_price[0] * percentage

    def is_15_day_high(self, day_price_list):
        return self._is_n_day_high(day_price_list, 15)

    def is_30_day_high(self, day_price_list):
        return self._is_n_day_high(day_price_list, 30)

    def is_60_day_high(self, day_price_list):
        return self._is_n_day_high(day_price_list, 60)

    def is_120_day_high(self, day_price_list):
        return self._is_n_day_high(day_price_list, 120)