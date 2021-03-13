from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=256,
                            verbose_name='Item Name')

    price = models.IntegerField(verbose_name='Item Price')

    description = models.TextField(verbose_name='Item Description')

    stock = models.IntegerField(verbose_name='Item Current Stock')

    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='Registered Date/Time')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'byun_project_product'
        verbose_name = 'Product'
