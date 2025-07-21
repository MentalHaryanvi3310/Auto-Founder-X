import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../lib/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if user is logged in on app start
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const savedUser = localStorage.getItem('user');
    
    if (token && savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
        setIsAuthenticated(true);
        
        // Verify token is still valid
        authAPI.getProfile()
          .then(response => {
            if (response.data.success) {
              setUser(response.data.user);
            }
          })
          .catch(() => {
            // Token is invalid, clear auth state
            logout();
          });
      } catch (error) {
        // Invalid saved data, clear it
        logout();
      }
    }
    
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await authAPI.login({ email, password });
      
      if (response.data.success) {
        const { token, user: userData } = response.data;
        
        // Save to localStorage
        localStorage.setItem('authToken', token);
        localStorage.setItem('user', JSON.stringify(userData));
        
        // Update state
        setUser(userData);
        setIsAuthenticated(true);
        
        return { success: true, user: userData };
      } else {
        return { success: false, message: response.data.message };
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Login failed';
      return { success: false, message };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData);
      
      if (response.data.success) {
        const { token, user: newUser } = response.data;
        
        // Save to localStorage
        localStorage.setItem('authToken', token);
        localStorage.setItem('user', JSON.stringify(newUser));
        
        // Update state
        setUser(newUser);
        setIsAuthenticated(true);
        
        return { success: true, user: newUser };
      } else {
        return { success: false, message: response.data.message };
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Registration failed';
      return { success: false, message };
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      // Continue with logout even if API call fails
      console.error('Logout API call failed:', error);
    }
    
    // Clear localStorage
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    
    // Update state
    setUser(null);
    setIsAuthenticated(false);
  };

  const updateProfile = async (profileData) => {
    try {
      const response = await authAPI.updateProfile(profileData);
      
      if (response.data.success) {
        const updatedUser = response.data.user;
        
        // Update localStorage
        localStorage.setItem('user', JSON.stringify(updatedUser));
        
        // Update state
        setUser(updatedUser);
        
        return { success: true, user: updatedUser };
      } else {
        return { success: false, message: response.data.message };
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Profile update failed';
      return { success: false, message };
    }
  };

  const changePassword = async (passwordData) => {
    try {
      const response = await authAPI.changePassword(passwordData);
      
      if (response.data.success) {
        return { success: true, message: response.data.message };
      } else {
        return { success: false, message: response.data.message };
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Password change failed';
      return { success: false, message };
    }
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    updateProfile,
    changePassword,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;

