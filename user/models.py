from django.db import models


class User(models.Model):

    username = models.CharField(max_length=64,
                                verbose_name='User Name')

    useremail = models.EmailField(max_length=128,
                                  verbose_name='User Email')

    password = models.CharField(max_length=128,
                                verbose_name='User Password')

    level = models.CharField(max_length=8,
                             verbose_name='User Level',
                             choices=(
                                 ('admin', 'admin'),
                                 ('user', 'user')),
                             default='user')

    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='Registered Date/Time')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'byun_project_user'
        verbose_name = 'User'
