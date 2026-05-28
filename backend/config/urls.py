from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/merchants/', include('merchants.urls')),
    path('api/analytics/', include('analytics.urls')),
]