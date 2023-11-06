from django.db import models

# Create your models here.

class Binary(models.Model):
    data = models.IntegerField()
    left = models.ForeignKey('self',on_delete=models.SET_NULL, related_name='left_child',null=True)
    right = models.ForeignKey('self',on_delete=models.SET_NULL, related_name='right_child',null=True)