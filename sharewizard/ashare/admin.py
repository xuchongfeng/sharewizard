from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Company
from .models import Trade
from .models import Strategy
from .models import Industry


class ControlCompany(admin.ModelAdmin):
    list_display = ('id', 'url', 'name', 'code', 'amount', 'value', 'industry')

    search_fields = ('name', 'code', 'industry')


class ControlTrade(admin.ModelAdmin):
    list_display = ('id', 'company', 't_date', 'high', 'low', 'open', 'close', 'amount', 'value', 'get_url')

    def get_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.company.url)

    get_url.short_description = "公司地址"

    search_fields = ('company', )


class ControlStrategy(admin.ModelAdmin):
    list_display = ('id', 'company', 't_date', 't_type', 'get_url')

    def get_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.company.url)

    get_url.short_description = "公司地址"

    search_fields = ('company', 't_date')
    list_filter = (
        ('t_date', admin.DateFieldListFilter),
        ('t_type', admin.ChoicesFieldListFilter),
        ('company__industry', admin.AllValuesFieldListFilter)
    )
    list_display_links = ('company', )


class ControlIndustry(admin.ModelAdmin):
    list_display = ('id', 'name', 't_date', 't_type', 'number')
    search_fields = ('name', 't_date')
    list_filter = (
        ('t_date', admin.DateFieldListFilter),
        ('t_type', admin.ChoicesFieldListFilter),
        ('name', admin.AllValuesFieldListFilter)
    )
    ordering = ("-number", )


admin.site.register(Company, ControlCompany)
admin.site.register(Trade, ControlTrade)
admin.site.register(Strategy, ControlStrategy)
admin.site.register(Industry, ControlIndustry)