from django.urls import path, include
from back_api import views

urlpatterns = [
  path('imports', views.ShopUnitView.as_view(), name='includes'),
  path('delete/<uuid:id>', views.shop_unit_delete, name='delete'),
  path('nodes/<uuid:id>', views.shop_unit_nodes),
  # path('sales', ),
  # path('node/<uuid:id>/statistic', ),
]
