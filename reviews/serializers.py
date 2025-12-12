from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for reviews
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'facility', 'facility_name', 
                  'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating reviews
    """
    class Meta:
        model = Review
        fields = ['facility', 'rating', 'comment']
    
    def validate(self, attrs):
        """
        Validate that owner cannot review own facility
        """
        user = self.context['request'].user
        facility = attrs['facility']
        
        if facility.owner == user:
            raise serializers.ValidationError({"facility": "You cannot review your own facility"})
        
        # Check if user has already reviewed this facility
        if Review.objects.filter(user=user, facility=facility).exists():
            raise serializers.ValidationError({"facility": "You have already reviewed this facility"})
        
        return attrs
    
    def create(self, validated_data):
        """
        Create review with current user
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating reviews
    """
    class Meta:
        model = Review
        fields = ['rating', 'comment']
