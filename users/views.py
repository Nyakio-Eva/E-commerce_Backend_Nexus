from django.shortcuts import render
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer, UserSerializer,ChangePasswordSerializer, ResetPasswordSerializer
from rest_framework import generics, permissions,status
from rest_framework.response import Response



class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user    


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
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get("email")
            try:
                user = User.objects.get(email=email)
                user.set_password(serializer.data.get("new_password"))
                user.save()
                return Response({"detail": "Password reset successful"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"email": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    