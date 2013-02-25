from django.db import models

# Create your models here.
class Flavour(models.Model):
    name = models.CharField(max_length=40)
    litres = models.FloatField() # How many litres we have in the store
    sellprice = models.DecimalField(decimal_places=2, max_digits=5) # How much it costs per litre

    def __unicode__(self):
        return self.name

