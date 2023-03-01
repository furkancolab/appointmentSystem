from django.db import models

# Create your models here.
class appointments(models.Model):
    psikolog=models.CharField(max_length=20,null=True)
    randevu_tarihi=models.CharField(max_length=70,null=True)
    randevu_saati=models.CharField(max_length=70,null=True)