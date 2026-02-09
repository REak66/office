import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Banner } from '../../shared/models/models';

@Injectable({
  providedIn: 'root'
})
export class BannerService {
  private apiUrl = `${environment.apiUrl}/banners`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<Banner[]> {
    return this.http.get<Banner[]>(this.apiUrl);
  }

  getActive(): Observable<Banner[]> {
    return this.http.get<Banner[]>(`${this.apiUrl}/active`);
  }

  getById(id: string): Observable<Banner> {
    return this.http.get<Banner>(`${this.apiUrl}/${id}`);
  }

  create(banner: Partial<Banner>): Observable<Banner> {
    return this.http.post<Banner>(this.apiUrl, banner);
  }

  update(id: string, banner: Partial<Banner>): Observable<Banner> {
    return this.http.put<Banner>(`${this.apiUrl}/${id}`, banner);
  }

  delete(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  toggleActive(id: string): Observable<Banner> {
    return this.http.patch<Banner>(`${this.apiUrl}/${id}/toggle`, {});
  }
}
