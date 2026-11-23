from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import MyTokenObtainPairView


urlpatterns = [
    path("", views.getQrng, name="qrng-root"),
    path("qrng/", views.getQrng, name="qrng"),
    path("getqrng_DecimalArray/", views.getqrng_DecimalArray),
    path("getQrngDecimal/", views.getQrngDecimalinrandom),
    path("getQrngHexArray/", views.getQrngHexArrayinrandom),
    path("mnemonic/", views.get_mnemonic_details),
    path("health/", views.health),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
