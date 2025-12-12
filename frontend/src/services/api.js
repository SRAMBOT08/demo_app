import axios from 'axios';

// Base API URL - Update this to match your Django backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;

// API Endpoints Export
export const endpoints = {
  // Auth
  login: '/auth/login/',
  register: '/auth/register/',
  logout: '/auth/logout/',
  profile: '/auth/profile/',
  
  // Facilities
  facilities: '/facilities/',
  facilityDetail: (id) => `/facilities/${id}/`,
  facilityApprove: (id) => `/facilities/${id}/approve/`,
  facilityReject: (id) => `/facilities/${id}/reject/`,
  
  // Bookings
  bookings: '/bookings/',
  bookingDetail: (id) => `/bookings/${id}/`,
  availableSlots: (id) => `/facilities/${id}/available-slots/`,
  
  // Matches (Match-making)
  matches: '/bookings/matches/',
  matchJoin: (id) => `/bookings/matches/${id}/join/`,
  matchLeave: (id) => `/bookings/matches/${id}/leave/`,
  
  // Reviews
  reviews: '/reviews/',
  facilityReviews: (id) => `/facilities/${id}/reviews/`,
  
  // Analytics
  analytics: '/analytics/',
  ownerEarnings: '/analytics/owner-earnings/',
  platformStats: '/analytics/platform-stats/',
  bookingTrends: '/analytics/booking-trends/',
  
  // Users (Admin)
  users: '/users/',
  userBan: (id) => `/users/${id}/ban/`,
  userUnban: (id) => `/users/${id}/unban/`,
};
