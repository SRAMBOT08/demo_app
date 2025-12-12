from rest_framework import serializers
from django.utils import timezone
from .models import Booking, Match, MatchParticipant
from facilities.serializers import FacilitySerializer


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for bookings
    """
    facility_details = FacilitySerializer(source='facility', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'user_name', 'facility', 'facility_details', 
                  'booking_date', 'start_time', 'end_time', 'total_price', 
                  'status', 'status_display', 'is_match', 'created_at', 'updated_at']
        read_only_fields = ['user', 'total_price', 'status', 'created_at', 'updated_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating bookings
    """
    class Meta:
        model = Booking
        fields = ['facility', 'booking_date', 'start_time', 'end_time', 'is_match']
    
    def validate(self, attrs):
        """
        Validate booking data
        """
        # Check if booking date is in the future
        if attrs['booking_date'] < timezone.now().date():
            raise serializers.ValidationError({"booking_date": "Cannot book in the past"})
        
        # Check if start_time is before end_time
        if attrs['start_time'] >= attrs['end_time']:
            raise serializers.ValidationError({"end_time": "End time must be after start time"})
        
        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            facility=attrs['facility'],
            booking_date=attrs['booking_date'],
            status__in=['pending', 'confirmed']
        ).filter(
            start_time__lt=attrs['end_time'],
            end_time__gt=attrs['start_time']
        )
        
        if overlapping.exists():
            raise serializers.ValidationError({"time": "This time slot is already booked"})
        
        return attrs
    
    def create(self, validated_data):
        """
        Calculate total price and create booking
        """
        facility = validated_data['facility']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']
        
        # Calculate duration in hours
        duration = (timezone.datetime.combine(timezone.datetime.today(), end_time) - 
                   timezone.datetime.combine(timezone.datetime.today(), start_time)).seconds / 3600
        
        validated_data['total_price'] = facility.price_per_hour * duration
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'confirmed'
        
        return super().create(validated_data)


class MatchParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer for match participants
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    skill_level = serializers.CharField(source='user.profile.skill_level', read_only=True)
    
    class Meta:
        model = MatchParticipant
        fields = ['id', 'user', 'user_name', 'skill_level', 'joined_at']
        read_only_fields = ['joined_at']


class MatchSerializer(serializers.ModelSerializer):
    """
    Serializer for matches
    """
    booking_details = BookingSerializer(source='booking', read_only=True)
    participants = MatchParticipantSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Match
        fields = ['id', 'booking', 'booking_details', 'created_by', 'created_by_name', 
                  'sport_type', 'max_participants', 'current_participants', 
                  'skill_level', 'description', 'is_public', 'is_full', 'participants']
        read_only_fields = ['created_by', 'current_participants', 'is_full']


class MatchCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating matches
    """
    booking_data = BookingCreateSerializer(write_only=True)
    
    class Meta:
        model = Match
        fields = ['booking_data', 'sport_type', 'max_participants', 'skill_level', 
                  'description', 'is_public']
    
    def create(self, validated_data):
        """
        Create booking and match together
        """
        booking_data = validated_data.pop('booking_data')
        booking_data['is_match'] = True
        
        # Create booking using BookingCreateSerializer
        booking_serializer = BookingCreateSerializer(
            data=booking_data, 
            context=self.context
        )
        booking_serializer.is_valid(raise_exception=True)
        booking = booking_serializer.save()
        
        # Create match
        match = Match.objects.create(
            booking=booking,
            created_by=self.context['request'].user,
            current_participants=1,
            **validated_data
        )
        
        # Add creator as first participant
        MatchParticipant.objects.create(
            match=match,
            user=self.context['request'].user
        )
        
        return match


class JoinMatchSerializer(serializers.Serializer):
    """
    Serializer for joining a match
    """
    match_id = serializers.IntegerField()
    
    def validate_match_id(self, value):
        """
        Validate match exists and is joinable
        """
        try:
            match = Match.objects.get(id=value)
        except Match.DoesNotExist:
            raise serializers.ValidationError("Match not found")
        
        if match.is_full:
            raise serializers.ValidationError("Match is full")
        
        if not match.is_public:
            raise serializers.ValidationError("Match is private")
        
        # Check if user already joined
        user = self.context['request'].user
        if match.participants.filter(user=user).exists():
            raise serializers.ValidationError("You have already joined this match")
        
        return value
