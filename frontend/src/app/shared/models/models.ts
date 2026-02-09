export interface User {
  _id: string;
  name: string;
  email: string;
  role: 'super_admin' | 'admin' | 'employee';
  avatar?: string;
  createdAt?: Date;
}

export interface LoginResponse {
  _id: string;
  name: string;
  email: string;
  role: string;
  avatar?: string;
  token: string;
}

export interface Employee {
  _id: string;
  name: string;
  email: string;
  position: string;
  department: string;
  phone?: string;
  address?: string;
  avatar?: string;
  userId?: any;
  createdAt?: Date;
}

export interface Attendance {
  _id: string;
  employeeId: Employee;
  date: Date;
  clockIn: string;
  clockOut: string;
  location: string;
  workDuration: string;
  type: 'WFO' | 'WFH';
  createdAt?: Date;
}

export interface Document {
  _id: string;
  title: string;
  description: string;
  submittedBy: User;
  status: 'awaiting_validation' | 'awaiting_verification' | 'closed' | 'completed' | 'awaiting_signature';
  category: string;
  createdAt?: Date;
}

export interface CircularLetter {
  _id: string;
  title: string;
  referenceNumber: string;
  priority: 'very_urgent' | 'urgent' | 'normal';
  content: string;
  date: Date;
  createdBy: User;
  createdAt?: Date;
}

export interface Banner {
  _id: string;
  title: string;
  description: string;
  imageUrl: string;
  isActive: boolean;
  createdAt?: Date;
}

export interface Event {
  _id: string;
  title: string;
  description: string;
  date: Date;
  location: string;
  createdBy: User;
  createdAt?: Date;
}

export interface News {
  _id: string;
  title: string;
  content: string;
  author: User;
  publishedDate: Date;
  createdAt?: Date;
}

export interface FileUpload {
  _id: string;
  fileName: string;
  originalName: string;
  path: string;
  size: number;
  uploadedBy: User;
  createdAt?: Date;
}

export interface DashboardSummary {
  totalEmployees: { count: number; change: number };
  employeeAbsence: { count: number; change: number };
  totalDocuments: { count: number; change: number };
  totalCirculars: { count: number; change: number };
}

export interface AttendanceSummary {
  month: string;
  present: number;
  absent: number;
}

export interface DocumentSubmission {
  total: number;
  breakdown: Array<{
    status: string;
    count: number;
    percentage: number;
  }>;
}
