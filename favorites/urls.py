from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('favorites/', views.FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/add/', views.FavoriteCreateView.as_view(), name='favorite-create'),
    path('favorites/<int:product_id>/', views.remove_favorite, name='favorite-remove'),
]
