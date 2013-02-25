from django.db import models

# Create your models here.
class Flavour(models.Model):
    name = models.CharField(max_length=40)
    litres = models.FloatField(help_text="How many litres do we have in the store?") 
    sellprice = models.DecimalField(decimal_places=2, max_digits=5, help_text="How much per litre?") # 

    def __unicode__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=60)
    favourite_flavour = models.ForeignKey(Flavour)

    def __unicode__(self):
        return self.name
