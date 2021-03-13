from django.db import models


class Order(models.Model):

    user = models.ForeignKey('user.User',
                             on_delete=models.CASCADE,
                             verbose_name='User')

    product = models.ForeignKey('product.Product',
                                on_delete=models.CASCADE,
                                verbose_name='Ordered Product')

    quantity = models.IntegerField(verbose_name='Item Quantity')

    status = models.CharField(
        choices=(
            ('On Hold', 'On Hold'),
            ('Processing', 'Processing'),
            ('Complete', 'Complete'),
            ('Refund', 'Refund'),
        ),
        default='On Hold',
        max_length=32,
        verbose_name='Status')

    memo = models.TextField(null=True, blank=True, verbose_name='Memo')

    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='Registered Date/Time')

    def __str__(self):
        return f"{self.user} - Item:{self.product} Quantity:{self.quantity}"

    class Meta:
        db_table = 'byun_project_order'
        verbose_name = 'Order'
