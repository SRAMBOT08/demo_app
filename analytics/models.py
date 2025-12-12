from django.db import models
from accounts.models import User
from facilities.models import Facility
from bookings.models import Booking

class BookingAnalytics(models.Model):
    """
    Aggregated booking analytics for reporting
    """
    date = models.DateField()
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='analytics', null=True, blank=True)
    total_bookings = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    cancelled_bookings = models.IntegerField(default=0)
    peak_hour = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'booking_analytics'
        unique_together = ['date', 'facility']
        ordering = ['-date']

    def __str__(self):
        if self.facility:
            return f"Analytics for {self.facility.name} on {self.date}"
        return f"Platform Analytics on {self.date}"


class OwnerEarnings(models.Model):
    """
    Track earnings for facility owners
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earnings')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='earnings')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='earnings')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'owner_earnings'
        ordering = ['-earned_at']

    def __str__(self):
        return f"Earning: {self.amount} for {self.owner.username}"
