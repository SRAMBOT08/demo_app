from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from math import radians, cos, sin, asin, sqrt
from .models import Facility, FacilityImage, FacilityAvailability
from .serializers import (
    FacilitySerializer, FacilityCreateSerializer, FacilityApprovalSerializer,
    FacilityImageSerializer, FacilityAvailabilitySerializer, FacilitySearchSerializer
)
from accounts.permissions import IsFacilityOwner, IsAdmin, IsOwner


class FacilityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for facility management
    """
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'sport_type', 'address']
    ordering_fields = ['created_at', 'rating', 'price_per_hour']
    
    def get_queryset(self):
        """
        Filter queryset based on user role
        """
        user = self.request.user
        queryset = Facility.objects.all()
        
        # Regular users only see approved facilities
        if not user.is_authenticated or user.role == 'user':
            queryset = queryset.filter(status='approved')
        # Owners see their own facilities
        elif user.role == 'owner':
            queryset = queryset.filter(Q(owner=user) | Q(status='approved'))
        # Admins see everything
        
        return queryset
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions
        """
        if self.action == 'create':
            return FacilityCreateSerializer
        return FacilitySerializer
    
    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action == 'create':
            return [IsFacilityOwner()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        elif self.action in ['approve', 'reject']:
            return [IsAdmin()]
        return super().get_permissions()
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """
        Advanced search with filters
        """
        serializer = FacilitySearchSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        queryset = self.get_queryset()
        
        # Filter by sport type
        if 'sport_type' in data:
            queryset = queryset.filter(sport_type=data['sport_type'])
        
        # Filter by price range
        if 'min_price' in data:
            queryset = queryset.filter(price_per_hour__gte=data['min_price'])
        if 'max_price' in data:
            queryset = queryset.filter(price_per_hour__lte=data['max_price'])
        
        # Filter by rating
        if 'min_rating' in data:
            queryset = queryset.filter(rating__gte=data['min_rating'])
        
        # Filter by location (radius search)
        if 'latitude' in data and 'longitude' in data:
            user_lat = float(data['latitude'])
            user_lon = float(data['longitude'])
            radius_km = float(data.get('radius_km', 10.0))
            
            # Filter facilities with location data
            facilities_with_location = queryset.exclude(
                latitude__isnull=True
            ).exclude(
                longitude__isnull=True
            )
            
            # Calculate distance for each facility
            nearby_facilities = []
            for facility in facilities_with_location:
                distance = self.calculate_distance(
                    user_lat, user_lon,
                    float(facility.latitude), float(facility.longitude)
                )
                
                if distance <= radius_km:
                    nearby_facilities.append(facility.id)
            
            queryset = queryset.filter(id__in=nearby_facilities)
        
        serializer = FacilitySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate distance between two coordinates using Haversine formula
        Returns distance in kilometers
        """
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        
        return km
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        """
        Approve a facility (admin only)
        """
        facility = self.get_object()
        facility.status = 'approved'
        facility.save()
        return Response({'message': 'Facility approved successfully'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def reject(self, request, pk=None):
        """
        Reject a facility (admin only)
        """
        facility = self.get_object()
        facility.status = 'rejected'
        facility.save()
        return Response({'message': 'Facility rejected'})
    
    @action(detail=True, methods=['get'])
    def available_slots(self, request, pk=None):
        """
        Get available time slots for a specific date
        """
        facility = self.get_object()
        date_str = request.query_params.get('date')
        
        if not date_str:
            return Response(
                {'error': 'Date parameter required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get availability and bookings for the date
        from bookings.models import Booking
        from datetime import datetime
        
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_of_week = date.weekday()
        
        # Get facility availability for that day
        availability = facility.availability.filter(
            day_of_week=day_of_week,
            is_available=True
        )
        
        # Get existing bookings
        bookings = Booking.objects.filter(
            facility=facility,
            booking_date=date,
            status__in=['pending', 'confirmed']
        )
        
        return Response({
            'availability': FacilityAvailabilitySerializer(availability, many=True).data,
            'bookings': [
                {
                    'start_time': b.start_time.strftime('%H:%M'),
                    'end_time': b.end_time.strftime('%H:%M')
                } for b in bookings
            ]
        })


class FacilityImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for facility images
    """
    queryset = FacilityImage.objects.all()
    serializer_class = FacilityImageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """
        Only facility owners can add/delete images
        """
        if self.action in ['create', 'destroy']:
            return [IsOwner()]
        return [IsAuthenticated()]


class FacilityAvailabilityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for facility availability
    """
    queryset = FacilityAvailability.objects.all()
    serializer_class = FacilityAvailabilitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """
        Only facility owners can manage availability
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return [IsAuthenticated()]
