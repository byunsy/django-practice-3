"""byun_project_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from user.views import index, logout, RegisterView, LoginView
from product.views import (ProductList, ProductCreate, ProductDetail,
                           ProductListAPI, ProductDetailAPI)
from order.views import OrderCreate, OrderList
from django.views.generic import TemplateView
from order.models import Order
import datetime


#  Customize Main Index Page.
orig_index = admin.site.index


def byun_proj_index(request, extra_context=None):
    base_date = datetime.datetime.now() - datetime.timedelta(days=7)
    order_data = {}
    for i in range(8):
        target_dttm = base_date + datetime.timedelta(days=i)
        date_key = target_dttm.strftime('%Y-%m-%d')
        target_date = datetime.date(
            target_dttm.year, target_dttm.month, target_dttm.day
        )
        order_cnt = Order.objects.filter(
            registered_dttm__date=target_date).count
        order_data[date_key] = order_cnt

    extra_context = {'orders': order_data}

    return orig_index(request, extra_context)


admin.site.index = byun_proj_index


urlpatterns = [
    re_path(r'^admin/manual/$',
            TemplateView.as_view(template_name='admin/manual.html',
                                 extra_context={
                                     'title': 'Manual',
                                     'site_title': 'Byun Project Backoffice',
                                     'site_header': 'Byun Project Backoffice',
                                 })),
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('', index),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
    path('product/', ProductList.as_view()),
    path('product/create/', ProductCreate.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('order/create/', OrderCreate.as_view()),
    path('order/', OrderList.as_view()),
    path('api/product/', ProductListAPI.as_view()),
    path('api/product/<int:pk>', ProductDetailAPI.as_view())
]
