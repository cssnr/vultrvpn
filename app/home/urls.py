from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('manage/', views.manage_view, name='manage'),
    path('create/', views.create_view, name='create'),
    path('delete/', views.delete_view, name='delete'),
    path('callback/', views.callback_view, name='callback'),
]
