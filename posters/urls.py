from django.urls import path
from . import views

urlpatterns = [
    path('quick_create', views.quick_create, name='quick_create'),
    path('simple_quick', views.simple_quick, name='simple_quick'),
    path('generate_poster/<path:bg_image_url>/<str:text_color>/<str:text1>/<str:text2>/<str:text3>/<str:text4>/', views.generate_poster, name='generate_poster'),
    path('generate_poster_two/', views.generate_poster_two, name='generate_poster_two'),
    # path('generate_poster', views.generate_poster, name='generate_poster'),


]