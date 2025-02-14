# from django.urls import path
# from . import views

# urlpatterns = [
#     path('upload/', views.upload_barcode, name='upload_barcode'),
#     path('add/<str:barcode>/', views.add_purchase, name='add_purchase'),

#     path('add/', views.add_purchase, name='add_purchase'),
#     # path('signup/', views.signup, name='signup'),
#     # path('signin/', views.signin_view, name='signin'),
#     # path('signout/', views.signout_view, name='signout'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_barcode, name='upload_barcode'),
    path('add/<str:barcode>/', views.add_purchase, name='add_purchase'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("export/csv/", views.export_purchases_csv, name="export_purchases_csv"), 

]
