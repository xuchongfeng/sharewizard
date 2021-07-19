from django.db import models


class Company(models.Model):
    class Meta:
        verbose_name_plural = '公司'

    actions = None

    name = models.CharField(verbose_name="名称", max_length=50)
    code = models.CharField(verbose_name="代码", max_length=24)
    value = models.CharField(verbose_name="市值", max_length=100)
    amount = models.CharField(verbose_name="股数", max_length=100)
    industry = models.CharField(verbose_name="行业", max_length=100)
    url = models.CharField(verbose_name="公司主页", max_length=1024)

    def __str__(self):
        return ",".join([self.name, self.code, self.value, self.amount, self.industry])


class Trade(models.Model):
    class Meta:
        verbose_name_plural = '每日交易数据'

    actions = None

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    t_date = models.DateField(verbose_name="交易日期")
    high = models.IntegerField(verbose_name="高点")
    low = models.IntegerField(verbose_name="低点")
    open = models.IntegerField(verbose_name="开盘价")
    close = models.IntegerField(verbose_name="收盘价")
    amount = models.CharField(verbose_name="交易数量", max_length=200)
    value = models.CharField(verbose_name="交易金额", max_length=200)

    def __str__(self):
        return ",".join(map(str, [self.t_date, self.high, self.low, self.open, self.close, self.amount, self.value]))


class Strategy(models.Model):
    class Meta:
        verbose_name_plural = '策略筛选'

    actions = None
    list_editable = False

    T_15_DAYS = 0
    T_30_DAYS = 1
    T_60_DAYS = 2
    T_120_DAYS = 3
    T_SHRINK = 4

    STRATEGY_TYPE = [
        (T_15_DAYS, "15日新高"),
        (T_30_DAYS, "30日新高"),
        (T_60_DAYS, "60日新高"),
        (T_120_DAYS, "120日新高"),
        (T_SHRINK, "收缩走势")
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    t_date = models.DateField(verbose_name="交易日期")
    t_type = models.IntegerField(verbose_name="策略类型", choices=STRATEGY_TYPE)

    def __str__(self):
        return ",".join(map(str, [self.company, self.t_date, self.t_type]))


class Industry(models.Model):
    class Meta:
        verbose_name_plural = '板块信息'

    T_15_DAYS = 0
    T_30_DAYS = 1
    T_60_DAYS = 2
    T_120_DAYS = 3
    T_SHRINK = 4

    STRATEGY_TYPE = [
        (T_15_DAYS, "15日新高"),
        (T_30_DAYS, "30日新高"),
        (T_60_DAYS, "60日新高"),
        (T_120_DAYS, "120日新高"),
        (T_SHRINK, "收缩走势")
    ]

    name = models.CharField(verbose_name="板块名称", max_length=100)
    t_date = models.DateField(verbose_name="统计日期")
    t_type = models.IntegerField(verbose_name="策略类型", choices=STRATEGY_TYPE)
    number = models.IntegerField(verbose_name="数量", default=0)




