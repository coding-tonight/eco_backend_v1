from django.urls import path
from . import views

urlpatterns = [
    path('colors/', views.ColorAPIView.as_view()),
    path('colors/<str:ref_id>/', views.ColorDetailApiView.as_view()),
    path('size/', views.SizeAPIView.as_view()),
    path('size/<str:ref_id>/', views.SizeDetailApiView.as_view()),
    # products section
    path('products/', views.ProductAPIView.as_view())
]