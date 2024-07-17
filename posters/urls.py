from django.urls import path
from . import views

urlpatterns = [
    path('quick_create', views.quick_create, name='quick_create'),
    path('details', views.details, name='details'),
    path('simple_quick', views.simple_quick, name='simple_quick'),
    path('generate_poster/', views.generate_poster, name='generate_poster'),
    # path('generate_poster', views.generate_poster, name='generate_poster'),


]