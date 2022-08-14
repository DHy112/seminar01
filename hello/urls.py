from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_post),
    path('test/', views.index),
    path('test/get_data', views.call_data)
]