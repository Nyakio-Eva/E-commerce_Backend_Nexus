from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Sum
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


from products.models import Product
from orders.models import Order

from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
)
from products.serializers import ProductListSerializer
from orders.serializers import OrderSerializer
from core.pagination import StandardResultsSetPagination

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
)

User = get_user_model()


# Registration (public)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]   


# Login (public)
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]  


# Profile (requires authentication)
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user    


# Change password (requires authentication)
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": "Wrong password."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(
                {"detail": "Password updated successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Reset password (public)
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]   

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get("email")
            try:
                user = User.objects.get(email=email)
                user.set_password(serializer.data.get("new_password"))
                user.save()
                return Response(
                    {"detail": "Password reset successful"},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {"email": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get(self, request):
        # Calculate dashboard metrics
        total_orders = Order.objects.count()
        total_sales = Order.objects.filter(
            status__in=[Order.CONFIRMED, Order.PROCESSING, Order.SHIPPED, Order.DELIVERED]
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        pending_orders = Order.objects.filter(status=Order.PENDING).count()
        total_products = Product.objects.filter(is_active=True).count()
        total_users = User.objects.filter(role=User.CUSTOMER).count()
        
        # Recent orders
        recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
        recent_orders_data = [{
            'id': order.id,
            'order_number': order.order_number,
            'user_email': order.user.email,
            'total_amount': order.total_amount,
            'status': order.status,
            'created_at': order.created_at
        } for order in recent_orders]
        
        # Low stock products
        low_stock_products = Product.objects.filter(
            is_active=True, stock__lte=10
        ).order_by('stock')[:10]
        
        low_stock_data = [{
            'id': product.id,
            'name': product.name,
            'stock': product.stock,
            'sku': product.sku
        } for product in low_stock_products]
        
        return Response({
            'metrics': {
                'total_orders': total_orders,
                'total_sales': total_sales,
                'pending_orders': pending_orders,
                'total_products': total_products,
                'total_users': total_users
            },
            'recent_orders': recent_orders_data,
            'low_stock_products': low_stock_data
        })

class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['email', 'username']
    ordering_fields = ['created_at', 'email']
    ordering = ['-created_at']

class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'user']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']

class LowStockProductsView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        threshold = self.request.query_params.get('threshold', 10)
        return Product.objects.filter(
            is_active=True,
            stock__lte=threshold
        ).order_by('stock')
