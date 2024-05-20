from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('jarvis_ticket.urls')),
    path('', include('simplyfox.urls')),
    path('admin/', admin.site.urls),
]
