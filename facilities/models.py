from django.db import models
from accounts.models import User

class Facility(models.Model):
    """
    Sports facility model with approval workflow
    """
    SPORT_TYPE_CHOICES = [
        ('badminton', 'Badminton'),
        ('tennis', 'Tennis'),
        ('basketball', 'Basketball'),
        ('football', 'Football'),
        ('cricket', 'Cricket'),
        ('volleyball', 'Volleyball'),
        ('table_tennis', 'Table Tennis'),
        ('swimming', 'Swimming'),
        ('gym', 'Gym'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='facilities')
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    sport_type = models.CharField(max_length=50, choices=SPORT_TYPE_CHOICES)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'facilities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.sport_type}"


class FacilityImage(models.Model):
    """
    Multiple images for a facility
    """
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='facilities/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'facility_images'

    def __str__(self):
        return f"Image for {self.facility.name}"


class FacilityAvailability(models.Model):
    """
    Availability schedule for facilities
    """
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'facility_availability'
        unique_together = ['facility', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.facility.name} - {self.get_day_of_week_display()}"
