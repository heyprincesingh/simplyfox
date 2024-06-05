from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('slack_channel_summary.urls')),
    path('admin/', admin.site.urls),
]
