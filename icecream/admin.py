from django.contrib import admin
from icecream.models import Flavour

# Override fields and ordering of fields
class FlavourAdmin(admin.ModelAdmin):
    fields = ['name', 'litres', 'sellprice']
    list_display = ('name', 'litres', 'sellprice')

admin.site.register(Flavour, FlavourAdmin)
