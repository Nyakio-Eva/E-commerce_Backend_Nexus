
from django.shortcuts import render
from rest_framework import generics,status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Import shared functionality from core
from core.pagination import StandardResultsSetPagination
from core.permissions import IsAdminOrReadOnly

# Local app imports
from .models import Favorite
from .serializers import (
    FavoriteSerializer,
    FavoriteCreateSerializer, 
    
)


# Create your views here.
class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

class FavoriteCreateView(generics.CreateAPIView):
    serializer_class = FavoriteCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                product_id=product_id
            )
            
            if created:
                return Response(
                    {'message': 'Product added to favorites'},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'message': 'Product already in favorites'},
                    status=status.HTTP_200_OK
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_favorite(request, product_id):
    try:
        favorite = Favorite.objects.get(user=request.user, product_id=product_id)
        favorite.delete()
        return Response({'message': 'Product removed from favorites'})
    except Favorite.DoesNotExist:
        return Response(
            {'error': 'Product not in favorites'},
            status=status.HTTP_404_NOT_FOUND
        )
