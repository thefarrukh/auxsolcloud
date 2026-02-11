from django.urls import path
from . import views

urlpatterns = [
    # ✅ BUGFIX: URL patterns to'g'rilandi
    path('chart-data/', views.get_chart_data, name='chart-data'),
    path('latest/', views.get_latest_data, name='latest-data'),  # ✅ QO'SHILDI
    path('statistics/', views.get_statistics, name='statistics'),  # ✅ QO'SHILDI
]