from rest_framework import serializers
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import BookingAnalytics, OwnerEarnings
from bookings.models import Booking


class BookingAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for booking analytics
    """
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    
    class Meta:
        model = BookingAnalytics
        fields = ['id', 'date', 'facility', 'facility_name', 'total_bookings', 
                  'total_revenue', 'cancelled_bookings', 'peak_hour', 'created_at']
        read_only_fields = ['created_at']


class OwnerEarningsSerializer(serializers.ModelSerializer):
    """
    Serializer for owner earnings
    """
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    booking_date = serializers.DateField(source='booking.booking_date', read_only=True)
    
    class Meta:
        model = OwnerEarnings
        fields = ['id', 'facility', 'facility_name', 'booking', 'booking_date', 
                  'amount', 'earned_at']
        read_only_fields = ['earned_at']


class BookingTrendsSerializer(serializers.Serializer):
    """
    Serializer for booking trends data
    """
    period = serializers.ChoiceField(choices=['daily', 'weekly', 'monthly'])
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    facility_id = serializers.IntegerField(required=False)


class EarningsSummarySerializer(serializers.Serializer):
    """
    Serializer for earnings summary
    """
    total_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_bookings = serializers.IntegerField()
    average_booking_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    period_start = serializers.DateField()
    period_end = serializers.DateField()


class PlatformAnalyticsSerializer(serializers.Serializer):
    """
    Serializer for platform-wide analytics
    """
    total_users = serializers.IntegerField()
    total_facilities = serializers.IntegerField()
    total_bookings = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    active_users = serializers.IntegerField()
    pending_facilities = serializers.IntegerField()
    bookings_this_month = serializers.IntegerField()
    revenue_this_month = serializers.DecimalField(max_digits=10, decimal_places=2)


class PeakHoursSerializer(serializers.Serializer):
    """
    Serializer for peak hours heatmap
    """
    hour = serializers.IntegerField()
    day_of_week = serializers.IntegerField()
    booking_count = serializers.IntegerField()
