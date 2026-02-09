import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { FileUpload } from '../../shared/models/models';

@Injectable({
  providedIn: 'root'
})
export class FileService {
  private apiUrl = `${environment.apiUrl}/files`;

  constructor(private http: HttpClient) {}

  upload(file: File): Observable<FileUpload> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<FileUpload>(`${this.apiUrl}/upload`, formData);
  }

  getAll(): Observable<FileUpload[]> {
    return this.http.get<FileUpload[]>(this.apiUrl);
  }

  getById(id: string): Observable<FileUpload> {
    return this.http.get<FileUpload>(`${this.apiUrl}/${id}`);
  }

  delete(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  download(id: string): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/${id}/download`, { responseType: 'blob' });
  }
}
