import axios from 'axios';
import { 
  Doctor, 
  Consultation, 
  UploadedDocument, 
  AIConversation, 
  GeneratedReport, 
  AuditLog,
  TokenResponse
} from '../types';

// Create Axios client with default configurations
const api = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to append JWT Access Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh upon expiration
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Check if error is unauthorized and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (refreshToken) {
        try {
          // Attempt token refresh
          const refreshRes = await axios.post<TokenResponse>(
            '/api/auth/refresh', 
            null, 
            { params: { refresh_token: refreshToken } }
          );
          
          const { access_token, refresh_token } = refreshRes.data;
          
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          
          // Retry the original request
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh token expired or invalid; clear session and force login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.reload();
        }
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: async (payload: any): Promise<TokenResponse> => {
    const res = await api.post<TokenResponse>('/api/auth/register', payload);
    return res.data;
  },
  login: async (payload: any): Promise<TokenResponse> => {
    const res = await api.post<TokenResponse>('/api/auth/login', payload);
    return res.data;
  },
};

export const doctorAPI = {
  getProfile: async (): Promise<Doctor> => {
    const res = await api.get<Doctor>('/api/doctors/me');
    return res.data;
  },
  updateProfile: async (payload: any): Promise<Doctor> => {
    const res = await api.put<Doctor>('/api/doctors/me', payload);
    return res.data;
  },
  getAuditLogs: async (): Promise<AuditLog[]> => {
    const res = await api.get<AuditLog[]>('/api/doctors/me/audit-logs');
    return res.data;
  },
};

export const consultationAPI = {
  create: async (payload: any): Promise<Consultation> => {
    const res = await api.post<Consultation>('/api/consultations', payload);
    return res.data;
  },
  list: async (): Promise<Consultation[]> => {
    const res = await api.get<Consultation[]>('/api/consultations');
    return res.data;
  },
  getDetails: async (id: number): Promise<Consultation> => {
    const res = await api.get<Consultation>(`/api/consultations/${id}`);
    return res.data;
  },
  close: async (id: number, payload: any): Promise<Consultation> => {
    const res = await api.post<Consultation>(`/api/consultations/${id}/close`, payload);
    return res.data;
  },
  delete: async (id: number): Promise<any> => {
    const res = await api.delete(`/api/consultations/${id}`);
    return res.data;
  },
};

export const ragAPI = {
  uploadDocument: async (consultationId: number, file: File): Promise<UploadedDocument> => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await api.post<UploadedDocument>(
      `/api/consultations/${consultationId}/upload`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return res.data;
  },
  getDocuments: async (consultationId: number): Promise<UploadedDocument[]> => {
    const res = await api.get<UploadedDocument[]>(`/api/consultations/${consultationId}/documents`);
    return res.data;
  },
  chat: async (consultationId: number, question: string): Promise<AIConversation> => {
    const res = await api.post<AIConversation>(`/api/consultations/${consultationId}/chat`, { question });
    return res.data;
  },
  getChatHistory: async (consultationId: number): Promise<AIConversation[]> => {
    const res = await api.get<AIConversation[]>(`/api/consultations/${consultationId}/chat-history`);
    return res.data;
  },
  generateReport: async (consultationId: number, payload: any): Promise<GeneratedReport> => {
    const res = await api.post<GeneratedReport>(`/api/consultations/${consultationId}/reports`, payload);
    return res.data;
  },
  getReports: async (consultationId: number): Promise<GeneratedReport[]> => {
    const res = await api.get<GeneratedReport[]>(`/api/consultations/${consultationId}/reports`);
    return res.data;
  },
};
