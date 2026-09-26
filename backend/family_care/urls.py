from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('family/', include('apps.members.urls')),
    path('records/', include('apps.records.urls')),
    path('medicines/', include('apps.medicines.urls')),
    path('appointments/', include('apps.appointments.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('predictions/', include('apps.predictions.urls')),
    path('emergency/', include('apps.emergency.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
