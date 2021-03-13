from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.html import format_html
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_format', 'styled_stock', 'registered_dttm')

    def price_format(self, obj):
        price = intcomma(obj.price)
        return f"$ {price}"

    def styled_stock(self, obj):
        if obj.stock <= 50:
            return format_html(f'<b><span style="color:red">{obj.stock}</span></b>')
        else:
            return obj.stock

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Product List'}
        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        product = Product.objects.get(pk=object_id)
        extra_context = {'title': f'{product.name}'}

        # Delete unnecessary save option buttons
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False

        return super().changeform_view(request, object_id, form_url, extra_context)

    styled_stock.short_description = 'Stock'
    price_format.short_description = 'Price'


admin.site.register(Product, ProductAdmin)
