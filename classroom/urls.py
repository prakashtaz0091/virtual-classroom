from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("main/", include("main.urls")),
    path("accounts/", include("account.urls")),
    path("common/", include("common.urls")),
    path("esewa-payment/", include("esewa_payment.urls")),
    path("v1/public/api/", include("apis.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
