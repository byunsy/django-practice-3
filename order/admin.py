from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.template.response import TemplateResponse
from django.db.models import F, Q
from django.db import transaction
from django.utils.html import format_html
from django.urls import path
from .models import Order
import datetime


def refund(modeladmin, request, queryset):

    with transaction.atomic():
        qs = queryset.filter(~Q(status='Refund'))
        ct = ContentType.objects.get_for_model(queryset.model)

        for obj in qs:
            obj.product.stock += obj.quantity
            obj.product.save()

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr='Order Refunds',
                action_flag=CHANGE,
                change_message="Order Refunds"
            )
        qs.update(status="Refund")


refund.short_description = 'Refund'


class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('user', 'product', 'quantity',
                    'styled_status', 'action', 'registered_dttm')
    change_list_template = 'admin/order_change_list.html'

    actions = [
        refund
    ]

    def action(self, obj):
        if obj.status != 'Refund':
            return format_html(f'<input type="button" value="Refund" onclick="order_refund_submit({obj.id})" class="btn btn-outline-primary btn-sm">')

    # For customizing backoffice
    def styled_status(self, obj):
        if obj.status == 'Refund':
            return format_html(f'<b><span style="color:red">{obj.status}</span></b>')
        if obj.status == 'Complete':
            return format_html(f'<b><span style="color:green">{obj.status}</span></b>')
        else:
            return obj.status

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Order List'}

        if request.method == 'POST':
            obj_id = request.POST.get('obj_id')

            if obj_id:
                qs = Order.objects.filter(pk=obj_id)
                ct = ContentType.objects.get_for_model(qs.model)

                for obj in qs:
                    obj.product.stock += obj.quantity
                    obj.product.save()

                    LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ct.pk,
                        object_id=obj.pk,
                        object_repr='Order Refunds',
                        action_flag=CHANGE,
                        change_message="Order Refunds"
                    )
                qs.update(status="Refund")

        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        order = Order.objects.get(pk=object_id)
        extra_context = {
            'title': f"{order.user.username}'s [{order.product.name}] order"}

        # Delete unnecessary save option buttons
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False

        return super().changeform_view(request, object_id, form_url, extra_context)

    styled_status.short_description = 'Status'

    def get_urls(self):
        urls = super().get_urls()
        date_urls = [
            path('date_view/', self.date_view)
        ]
        return date_urls + urls

    def date_view(self, request):
        week_date = datetime.datetime.now() - datetime.timedelta(days=8)
        week_data = Order.objects.filter(registered_dttm__gte=week_date)
        other_data = Order.objects.filter(registered_dttm__lt=week_date)
        context = dict(
            self.admin_site.each_context(request),
            week_data=week_data,
            other_data=other_data,
        )
        return TemplateResponse(request, 'admin/order_date_view.html', context)


admin.site.register(Order, OrderAdmin)
