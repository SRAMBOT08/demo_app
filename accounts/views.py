from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .models import UserProfile
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserProfileUpdateSerializer,
    PasswordChangeSerializer
)
from .permissions import IsAdmin

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    """
    ViewSet for authentication (login, register, logout)
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Register a new user
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Login user and return JWT tokens
        """
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if user.is_banned:
            return Response(
                {'error': 'Your account has been banned'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        Logout user by blacklisting refresh token
        """
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """
        Admin only for list/destroy, authenticated users for retrieve/update
        """
        if self.action in ['list', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def profile(self, request):
        """
        Get or update current user profile
        """
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        
        # Update profile
        profile_serializer = UserProfileUpdateSerializer(
            request.user.profile, 
            data=request.data, 
            partial=True
        )
        
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(UserSerializer(request.user).data)
        
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Change user password
        """
        serializer = PasswordChangeSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': 'Incorrect password'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({'message': 'Password changed successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def ban(self, request, pk=None):
        """
        Ban a user (admin only)
        """
        user = self.get_object()
        user.is_banned = True
        user.save()
        return Response({'message': f'User {user.username} has been banned'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def unban(self, request, pk=None):
        """
        Unban a user (admin only)
        """
        user = self.get_object()
        user.is_banned = False
        user.save()
        return Response({'message': f'User {user.username} has been unbanned'})
