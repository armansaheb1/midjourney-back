from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('api/adminpanel/', include('admin.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
