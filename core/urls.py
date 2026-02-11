from django.contrib import admin
from django.urls import path, include  # include qo'shildi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Sizning API yo'llaringiz (bu yerda hamma amallaringiz ko'rinadi)
    path('api/', include('auxsol_app.urls')),

    # 2. Swagger uchun texnik qismlar
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]