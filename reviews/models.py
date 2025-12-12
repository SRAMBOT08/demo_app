from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from facilities.models import Facility

class Review(models.Model):
    """
    Review and rating model for facilities
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
        # One review per user per facility
        unique_together = ['user', 'facility']

    def __str__(self):
        return f"Review by {self.user.username} for {self.facility.name}"
    
    def save(self, *args, **kwargs):
        """
        Update facility rating when review is saved
        """
        super().save(*args, **kwargs)
        self.update_facility_rating()
    
    def update_facility_rating(self):
        """
        Recalculate facility average rating
        """
        facility = self.facility
        reviews = facility.reviews.all()
        if reviews.exists():
            avg_rating = sum(r.rating for r in reviews) / reviews.count()
            facility.rating = round(avg_rating, 2)
            facility.total_reviews = reviews.count()
            facility.save()
