from django.urls import path 

from . import views


urlpatterns = [
    path('metadata/', views.MetaDataAPI.as_view()),
    path('metadata/<str:ref_id>/', views.MetaDataDetailAPI.as_view())
] 