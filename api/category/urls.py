from django.urls import path

from . import views

urlpatterns = [
    path('category/all/', views.CategoryApi.as_view()),
    path('category/', views.AddCategoryApi.as_view()),
    path('category/<str:ref_id>/', views.CategoryDetail.as_view())
]
