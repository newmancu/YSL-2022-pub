from django.contrib import admin
from back_api.models import ShopUnitBase, ShopUnitHistory

# Register your models here.
class ShopUnitAdmin(admin.ModelAdmin):
  pass

class ShopUnitHistoryAdmin(admin.ModelAdmin):
  pass


admin.site.register(ShopUnitBase, ShopUnitAdmin)
admin.site.register(ShopUnitHistory, ShopUnitHistoryAdmin)