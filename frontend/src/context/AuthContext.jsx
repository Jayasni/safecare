import { createContext, useCallback, useContext, useEffect, useState } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const applyToken = useCallback((newToken) => {
    setToken(newToken);
    if (newToken) {
      api.defaults.headers.common.Authorization = `Bearer ${newToken}`;
    } else {
      delete api.defaults.headers.common.Authorization;
    }
  }, []);

  const refresh = useCallback(async () => {
    try {
      const response = await api.post('/auth/refresh');
      applyToken(response.data.access_token);
      setUser(response.data.user);
      return true;
    } catch {
      applyToken(null);
      setUser(null);
      return false;
    }
  }, [applyToken]);

  useEffect(() => {
    (async () => {
      await refresh();
      setIsLoading(false);
    })();
  }, [refresh]);

  const login = useCallback(async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    applyToken(response.data.access_token);
    setUser(response.data.user);
    return response.data;
  }, [applyToken]);

  const register = useCallback(async (payload) => {
    const response = await api.post('/auth/register', payload);
    return response.data;
  }, []);

  const logout = useCallback(async () => {
    try {
      await api.post('/auth/logout');
    } catch {
      // Ignore logout transport errors and clear local state.
    }
    applyToken(null);
    setUser(null);
  }, [applyToken]);

  const value = {
    user,
    token,
    isLoading,
    isAuthenticated: Boolean(user && token),
    login,
    register,
    logout,
    refresh,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider');
  }
  return context;
}