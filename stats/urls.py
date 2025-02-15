from django.urls import path
from . import views


urlpatterns = [
    path('', views.stats_view, name='stats'),
    path('data/', views.stats_data, name='stats_data'),
    path("send-report/", views.send_report_email, name="send_report"),
]
