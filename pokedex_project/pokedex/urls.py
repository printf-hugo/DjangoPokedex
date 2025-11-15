from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('api/favorites/', views.api_favorites, name='api_favorites'),
    path('api/favorites/<int:favorite_id>/', views.api_favorite_detail, name='api_favorite_detail'),
]