from django.urls import path
# from .views import stats_view, stats_data
from . import views

urlpatterns = [
    path('', views.stats_view, name='stats'),
    path('data/', views.stats_data, name='stats_data'),  # ✅ Endpoint for fetching data
    path("send-report/", views.send_report_email, name="send_report"),
]
