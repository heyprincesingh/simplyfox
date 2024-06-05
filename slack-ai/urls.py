from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('slack_summary.urls')),
    path('admin/', admin.site.urls),
]
