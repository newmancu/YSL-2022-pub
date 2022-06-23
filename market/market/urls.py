from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),    # default django admin page
    path('', include('back_api.urls'))
]
