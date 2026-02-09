import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { CircularLetter } from '../../shared/models/models';

@Injectable({
  providedIn: 'root'
})
export class CircularService {
  private apiUrl = `${environment.apiUrl}/circulars`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }

  getById(id: string): Observable<CircularLetter> {
    return this.http.get<CircularLetter>(`${this.apiUrl}/${id}`);
  }

  create(circular: Partial<CircularLetter>): Observable<CircularLetter> {
    return this.http.post<CircularLetter>(this.apiUrl, circular);
  }

  update(id: string, circular: Partial<CircularLetter>): Observable<CircularLetter> {
    return this.http.put<CircularLetter>(`${this.apiUrl}/${id}`, circular);
  }

  delete(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
