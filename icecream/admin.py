from django.contrib import admin
from icecream.models import Flavour, Person

# Override fields and ordering of fields
class FlavourAdmin(admin.ModelAdmin):
    fields = ['name', 'litres', 'sellprice']
    list_display = ('name', 'litres', 'sellprice')

class PersonAdmin(admin.ModelAdmin):
    fields = ['name', 'favourite_flavour']
    list_display = ('name', 'favourite_flavour')

admin.site.register(Flavour, FlavourAdmin)
admin.site.register(Person, PersonAdmin)
