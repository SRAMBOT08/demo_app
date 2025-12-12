import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LoadingSpinner from './LoadingSpinner';

const ProtectedRoute = ({ children, requiredRole }) => {
  const { user, loading, isAuthenticated } = useAuth();

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  // Check role if required
  if (requiredRole && user?.role !== requiredRole) {
    // Redirect to appropriate dashboard based on user role
    const redirectMap = {
      admin: '/admin/dashboard',
      owner: '/owner/dashboard',
      user: '/user/dashboard',
    };
    return <Navigate to={redirectMap[user?.role] || '/'} replace />;
  }

  return children;
};

export default ProtectedRoute;
