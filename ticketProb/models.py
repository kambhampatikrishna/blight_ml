from django.db import models

# Create your models here.
class BlightModel(models.Model):
    ticket_id=models.IntegerField()
    probability=models.FloatField()
