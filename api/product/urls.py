from django.urls import path

from . import views

urlpatterns = [
    path('admin/colors/', views.ColorApiView.as_view()),
    path('tags/', views.TagsApiView.as_view()),
    path('products/', views.ProductApiView.as_view())
]