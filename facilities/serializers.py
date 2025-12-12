from rest_framework import serializers
from .models import Facility, FacilityImage, FacilityAvailability


class FacilityImageSerializer(serializers.ModelSerializer):
    """
    Serializer for facility images
    """
    class Meta:
        model = FacilityImage
        fields = ['id', 'image', 'is_primary', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class FacilityAvailabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for facility availability
    """
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = FacilityAvailability
        fields = ['id', 'day_of_week', 'day_name', 'start_time', 'end_time', 'is_available']


class FacilitySerializer(serializers.ModelSerializer):
    """
    Serializer for facility with owner and images
    """
    images = FacilityImageSerializer(many=True, read_only=True)
    availability = FacilityAvailabilitySerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    sport_type_display = serializers.CharField(source='get_sport_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Facility
        fields = ['id', 'owner', 'owner_name', 'name', 'description', 'address', 
                  'latitude', 'longitude', 'sport_type', 'sport_type_display', 
                  'price_per_hour', 'status', 'status_display', 'rating', 
                  'total_reviews', 'images', 'availability', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'status', 'rating', 'total_reviews', 'created_at', 'updated_at']


class FacilityCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating facilities
    """
    class Meta:
        model = Facility
        fields = ['name', 'description', 'address', 'latitude', 'longitude', 
                  'sport_type', 'price_per_hour']
    
    def create(self, validated_data):
        """
        Set owner from request user
        """
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class FacilityApprovalSerializer(serializers.ModelSerializer):
    """
    Serializer for admin to approve/reject facilities
    """
    class Meta:
        model = Facility
        fields = ['status']
    
    def validate_status(self, value):
        """
        Ensure status is only approved or rejected
        """
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError("Status must be 'approved' or 'rejected'")
        return value


class FacilitySearchSerializer(serializers.Serializer):
    """
    Serializer for facility search filters
    """
    sport_type = serializers.ChoiceField(choices=Facility.SPORT_TYPE_CHOICES, required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    radius_km = serializers.FloatField(required=False, default=10.0)
    min_rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False)
