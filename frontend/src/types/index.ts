export interface Doctor {
  id: number;
  email: string;
  full_name: string;
  specialty?: string;
  created_at: string;
}

export interface Consultation {
  id: number;
  doctor_id: number;
  patient_name: string;
  patient_age: number;
  patient_gender: string;
  status: 'active' | 'completed';
  summary?: string;
  created_at: string;
  updated_at: string;
}

export interface UploadedDocument {
  id: number;
  consultation_id: number;
  filename: string;
  file_path: string;
  file_type: string;
  created_at: string;
}

export interface AIConversation {
  id: number;
  consultation_id: number;
  question: string;
  answer: string;
  confidence_score?: number;
  evidence?: any[];
  citations?: any[];
  created_at: string;
}

export interface GeneratedReport {
  id: number;
  consultation_id: number;
  content: string;
  report_type: string;
  created_at: string;
}

export interface AuditLog {
  id: number;
  doctor_id?: number;
  action: string;
  ip_address?: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
