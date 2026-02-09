import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { DocumentService } from '../../core/services/document.service';
import { Document } from '../../shared/models/models';

@Component({
  selector: 'app-documents',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="page">
      <div class="page-header">
        <h1>Document Management</h1>
        <button class="btn-primary" (click)="showForm = true" *ngIf="!showForm">+ Add Document</button>
      </div>
      <div class="card form-card" *ngIf="showForm">
        <h2>{{ editingId ? 'Edit' : 'Add' }} Document</h2>
        <form [formGroup]="form" (ngSubmit)="onSubmit()">
          <div class="form-group">
            <label>Title</label>
            <input type="text" formControlName="title" class="form-control">
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea formControlName="description" class="form-control" rows="4"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Category</label>
              <input type="text" formControlName="category" class="form-control">
            </div>
            <div class="form-group">
              <label>Status</label>
              <select formControlName="status" class="form-control">
                <option value="awaiting_validation">Awaiting Validation</option>
                <option value="awaiting_verification">Awaiting Verification</option>
                <option value="awaiting_signature">Awaiting Signature</option>
                <option value="completed">Completed</option>
                <option value="closed">Closed</option>
              </select>
            </div>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-secondary" (click)="cancel()">Cancel</button>
            <button type="submit" class="btn-primary" [disabled]="form.invalid">Save</button>
          </div>
        </form>
      </div>
      <div class="card">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Description</th>
              <th>Category</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let item of items">
              <td>{{ item.title }}</td>
              <td>{{ item.description }}</td>
              <td>{{ item.category }}</td>
              <td><span class="badge">{{ item.status.replace('_', ' ') }}</span></td>
              <td class="actions">
                <button class="btn-icon" (click)="edit(item)">✏️</button>
                <button class="btn-icon" (click)="delete(item._id)">🗑️</button>
              </td>
            </tr>
            <tr *ngIf="items.length === 0"><td colspan="5" class="empty">No records found</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  `,
  styleUrls: ['../employees/employees.component.scss']
})
export class DocumentsComponent implements OnInit {
  items: Document[] = [];
  showForm = false;
  form: FormGroup;
  editingId: string | null = null;

  constructor(private fb: FormBuilder, private service: DocumentService) {
    this.form = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      category: ['', Validators.required],
      status: ['awaiting_validation', Validators.required]
    });
  }

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.service.getAll().subscribe(data => this.items = data.documents || data);
  }

  edit(item: Document): void {
    this.showForm = true;
    this.editingId = item._id;
    this.form.patchValue(item);
  }

  delete(id: string): void {
    if (confirm('Are you sure?')) {
      this.service.delete(id).subscribe(() => this.load());
    }
  }

  onSubmit(): void {
    if (this.form.valid) {
      const req = this.editingId
        ? this.service.update(this.editingId, this.form.value)
        : this.service.create(this.form.value);
      req.subscribe(() => {
        this.load();
        this.showForm = false;
      });
    }
  }

  cancel(): void {
    this.showForm = false;
    this.form.reset();
  }
}
