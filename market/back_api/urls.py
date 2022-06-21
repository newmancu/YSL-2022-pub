from django.urls import path
from back_api import views


urlpatterns = [
  path('imports', views.ShopUnitView.as_view(), name='includes'),
  path('delete/<uuid:id>', views.shop_unit_delete, name='delete'),
  path('nodes/<uuid:id>', views.shop_unit_nodes, name='nodes'),
  path('sales', views.shop_unit_sales, name='sales'),
  path('node/<uuid:id>/statistic', views.shop_unit_node_statistic, name='node_statistic'),
]
