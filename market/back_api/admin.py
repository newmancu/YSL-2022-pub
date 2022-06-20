from django.contrib import admin
from back_api.models import ShopUnitBase

# Register your models here.
class ShopUnitAdmin(admin.ModelAdmin):
  pass

admin.site.register(ShopUnitBase, ShopUnitAdmin)