from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('<int:product_id>/reviews/', views.ProductReviewListCreateView.as_view(), name='product-reviews'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]
