import api, { endpoints } from './api';

// Authentication Service
export const authService = {
  // Login
  login: async (credentials) => {
    const response = await api.post(endpoints.login, credentials);
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  // Register
  register: async (userData) => {
    const response = await api.post(endpoints.register, userData);
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  // Logout
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  // Get current user
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Get profile
  getProfile: async () => {
    const response = await api.get(endpoints.profile);
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  },

  // Update profile
  updateProfile: async (profileData) => {
    const response = await api.put(endpoints.profile, profileData);
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  },

  // Check if authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },

  // Get user role
  getUserRole: () => {
    const user = authService.getCurrentUser();
    return user?.role || 'user';
  },
};

// Facilities Service
export const facilitiesService = {
  // Get all facilities
  getAll: async (params) => {
    const response = await api.get(endpoints.facilities, { params });
    return response.data;
  },

  // Get facility by ID
  getById: async (id) => {
    const response = await api.get(endpoints.facilityDetail(id));
    return response.data;
  },

  // Create facility (Owner)
  create: async (facilityData) => {
    const response = await api.post(endpoints.facilities, facilityData);
    return response.data;
  },

  // Update facility (Owner)
  update: async (id, facilityData) => {
    const response = await api.put(endpoints.facilityDetail(id), facilityData);
    return response.data;
  },

  // Delete facility (Owner)
  delete: async (id) => {
    const response = await api.delete(endpoints.facilityDetail(id));
    return response.data;
  },

  // Approve facility (Admin)
  approve: async (id) => {
    const response = await api.post(endpoints.facilityApprove(id));
    return response.data;
  },

  // Reject facility (Admin)
  reject: async (id) => {
    const response = await api.post(endpoints.facilityReject(id));
    return response.data;
  },

  // Get available slots
  getAvailableSlots: async (id, date) => {
    const response = await api.get(endpoints.availableSlots(id), {
      params: { date },
    });
    return response.data;
  },
};

// Bookings Service
export const bookingsService = {
  // Get all bookings
  getAll: async (params) => {
    const response = await api.get(endpoints.bookings, { params });
    return response.data;
  },

  // Get booking by ID
  getById: async (id) => {
    const response = await api.get(endpoints.bookingDetail(id));
    return response.data;
  },

  // Create booking
  create: async (bookingData) => {
    const response = await api.post(endpoints.bookings, bookingData);
    return response.data;
  },

  // Cancel booking
  cancel: async (id) => {
    const response = await api.delete(endpoints.bookingDetail(id));
    return response.data;
  },

  // Get matches (match-making)
  getMatches: async (params) => {
    const response = await api.get(endpoints.matches, { params });
    return response.data;
  },

  // Join match
  joinMatch: async (id) => {
    const response = await api.post(endpoints.matchJoin(id));
    return response.data;
  },

  // Leave match
  leaveMatch: async (id) => {
    const response = await api.post(endpoints.matchLeave(id));
    return response.data;
  },
};

// Reviews Service
export const reviewsService = {
  // Get all reviews
  getAll: async (params) => {
    const response = await api.get(endpoints.reviews, { params });
    return response.data;
  },

  // Get reviews for facility
  getFacilityReviews: async (facilityId) => {
    const response = await api.get(endpoints.facilityReviews(facilityId));
    return response.data;
  },

  // Create review
  create: async (reviewData) => {
    const response = await api.post(endpoints.reviews, reviewData);
    return response.data;
  },

  // Update review
  update: async (id, reviewData) => {
    const response = await api.put(`${endpoints.reviews}${id}/`, reviewData);
    return response.data;
  },

  // Delete review
  delete: async (id) => {
    const response = await api.delete(`${endpoints.reviews}${id}/`);
    return response.data;
  },
};

// Analytics Service
export const analyticsService = {
  // Get analytics dashboard
  getDashboard: async () => {
    const response = await api.get(endpoints.analytics);
    return response.data;
  },

  // Get owner earnings
  getOwnerEarnings: async (params) => {
    const response = await api.get(endpoints.ownerEarnings, { params });
    return response.data;
  },

  // Get platform stats (Admin)
  getPlatformStats: async () => {
    const response = await api.get(endpoints.platformStats);
    return response.data;
  },

  // Get booking trends
  getBookingTrends: async (params) => {
    const response = await api.get(endpoints.bookingTrends, { params });
    return response.data;
  },
};

// Users Service (Admin)
export const usersService = {
  // Get all users
  getAll: async (params) => {
    const response = await api.get(endpoints.users, { params });
    return response.data;
  },

  // Ban user
  ban: async (id) => {
    const response = await api.post(endpoints.userBan(id));
    return response.data;
  },

  // Unban user
  unban: async (id) => {
    const response = await api.post(endpoints.userUnban(id));
    return response.data;
  },
};
