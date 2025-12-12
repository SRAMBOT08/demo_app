from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
from facilities.models import Facility

class Booking(models.Model):
    """
    Booking model with double-booking prevention
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_match = models.BooleanField(default=False)  # For match-making feature
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
        # Prevent double booking at database level
        unique_together = ['facility', 'booking_date', 'start_time']

    def __str__(self):
        return f"Booking by {self.user.username} at {self.facility.name}"
    
    def clean(self):
        """
        Validate that booking times don't overlap
        """
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")
        
        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            facility=self.facility,
            booking_date=self.booking_date,
            status__in=['pending', 'confirmed']
        ).exclude(id=self.id)
        
        for booking in overlapping:
            if (self.start_time < booking.end_time and self.end_time > booking.start_time):
                raise ValidationError("This time slot overlaps with an existing booking")


class Match(models.Model):
    """
    Match-making feature for public matches
    """
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='match')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_matches')
    sport_type = models.CharField(max_length=50)
    max_participants = models.IntegerField(default=4)
    current_participants = models.IntegerField(default=1)
    skill_level = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    is_full = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'matches'

    def __str__(self):
        return f"Match at {self.booking.facility.name} - {self.current_participants}/{self.max_participants}"


class MatchParticipant(models.Model):
    """
    Participants in a match
    """
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_participations')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'match_participants'
        unique_together = ['match', 'user']

    def __str__(self):
        return f"{self.user.username} in match at {self.match.booking.facility.name}"
