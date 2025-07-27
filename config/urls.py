from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from factures.views import errors

handler403 = errors.handler403
handler404 = errors.handler404
handler405 = errors.handler405
handler500 = errors.handler500


urlpatterns = [
    path('auser/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('payment/', include('payment.urls')),
    path('', include('factures.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
