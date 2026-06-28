import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Doctor, TokenResponse } from '../types';
import { authAPI, doctorAPI } from '../services/api';

interface AuthContextType {
  doctor: Doctor | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, full_name: string, specialty?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [doctor, setDoctor] = useState<Doctor | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      doctorAPI.getProfile()
        .then(setDoctor)
        .catch(() => {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const storeTokens = (tokens: TokenResponse) => {
    localStorage.setItem('access_token', tokens.access_token);
    localStorage.setItem('refresh_token', tokens.refresh_token);
  };

  const login = async (email: string, password: string) => {
    const tokens = await authAPI.login({ email, password });
    storeTokens(tokens);
    const profile = await doctorAPI.getProfile();
    setDoctor(profile);
  };

  const register = async (email: string, password: string, full_name: string, specialty?: string) => {
    const tokens = await authAPI.register({ email, password, full_name, specialty });
    storeTokens(tokens);
    const profile = await doctorAPI.getProfile();
    setDoctor(profile);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setDoctor(null);
  };

  return (
    <AuthContext.Provider value={{ doctor, isAuthenticated: !!doctor, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
