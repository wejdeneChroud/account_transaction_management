
from django.contrib import admin
from django.urls import path, include
from bank import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bank/', include(urls))
]
