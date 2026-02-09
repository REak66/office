import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { DashboardSummary, AttendanceSummary, DocumentSubmission } from '../../shared/models/models';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private apiUrl = `${environment.apiUrl}/dashboard`;

  constructor(private http: HttpClient) {}

  getSummary(): Observable<DashboardSummary> {
    return this.http.get<DashboardSummary>(`${this.apiUrl}/summary`);
  }

  getAttendanceSummary(): Observable<AttendanceSummary[]> {
    return this.http.get<AttendanceSummary[]>(`${this.apiUrl}/attendance-summary`);
  }

  getDocumentSubmission(): Observable<DocumentSubmission> {
    return this.http.get<DocumentSubmission>(`${this.apiUrl}/document-submission`);
  }
}
