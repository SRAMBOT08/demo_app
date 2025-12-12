from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission to only allow owners of an object to edit it
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.role == 'admin'


class IsFacilityOwner(permissions.BasePermission):
    """
    Permission for facility owners
    """
    def has_permission(self, request, view):
        return request.user.role in ['owner', 'admin']


class IsAdmin(permissions.BasePermission):
    """
    Permission for admin users only
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Read-only for everyone, write for authenticated users
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


class CannotReviewOwnFacility(permissions.BasePermission):
    """
    Prevent facility owners from reviewing their own facilities
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            facility_id = request.data.get('facility')
            if facility_id:
                from facilities.models import Facility
                try:
                    facility = Facility.objects.get(id=facility_id)
                    return facility.owner != request.user
                except Facility.DoesNotExist:
                    return True
        return True
