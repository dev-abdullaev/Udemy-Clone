from django.db import models



class Payment(models.Model):
    card_number = models.IntegerField()
    expire_date = models.DateField()
    security_number = models.IntegerField()