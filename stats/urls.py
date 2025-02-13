from django.urls import path
from .views import stats_view, stats_data

urlpatterns = [
    path('', stats_view, name='stats'),
    path('data/', stats_data, name='stats_data'),  # ✅ Endpoint for fetching data
]
