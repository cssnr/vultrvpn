# from django.db import models
#
#
# class Instances(models.Model):
#     api_token = models.CharField(unique=True, max_length=36, verbose_name='API Token')
#     instance_id = models.CharField(unique=True, max_length=38, verbose_name='Instance ID')
#     session_id = models.CharField(unique=True, max_length=32, verbose_name='Main Class')
#     password = models.CharField(null=True, max_length=32, verbose_name='VPN Password')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'{self.instance_id}'
#
#     class Meta:
#         verbose_name = 'Instances'
#         verbose_name_plural = 'Instances'
