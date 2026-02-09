import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FileService } from '../../core/services/file.service';
import { FileUpload } from '../../shared/models/models';

@Component({
  selector: 'app-file-mgmt',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="page">
      <div class="page-header">
        <h1>File Management</h1>
        <input type="file" #fileInput (change)="onFileSelect($event)" style="display: none">
        <button class="btn-primary" (click)="fileInput.click()">+ Upload File</button>
      </div>
      <div class="card">
        <table>
          <thead>
            <tr>
              <th>File Name</th>
              <th>Original Name</th>
              <th>Size</th>
              <th>Uploaded By</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let item of items">
              <td>{{ item.fileName }}</td>
              <td>{{ item.originalName }}</td>
              <td>{{ (item.size / 1024).toFixed(2) }} KB</td>
              <td>{{ item.uploadedBy?.name || 'N/A' }}</td>
              <td>{{ item.createdAt | date:'short' }}</td>
              <td class="actions">
                <button class="btn-icon" (click)="download(item._id)">⬇️</button>
                <button class="btn-icon" (click)="delete(item._id)">🗑️</button>
              </td>
            </tr>
            <tr *ngIf="items.length === 0"><td colspan="6" class="empty">No files found</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  `,
  styleUrls: ['../employees/employees.component.scss']
})
export class FileMgmtComponent implements OnInit {
  items: FileUpload[] = [];

  constructor(private service: FileService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.service.getAll().subscribe(data => this.items = data);
  }

  onFileSelect(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.service.upload(file).subscribe(() => {
        this.load();
        event.target.value = '';
      });
    }
  }

  download(id: string): void {
    this.service.download(id).subscribe(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'file';
      a.click();
    });
  }

  delete(id: string): void {
    if (confirm('Are you sure?')) {
      this.service.delete(id).subscribe(() => this.load());
    }
  }
}
