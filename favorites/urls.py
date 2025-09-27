from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('', views.FavoriteListView.as_view(), name='favorite-list'),
    path('add/', views.FavoriteCreateView.as_view(), name='favorite-create'),
    path('<int:product_id>/', views.remove_favorite, name='favorite-remove'),
]
