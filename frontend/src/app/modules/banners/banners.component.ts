import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { BannerService } from '../../core/services/banner.service';
import { Banner } from '../../shared/models/models';

@Component({
  selector: 'app-banners',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="page">
      <div class="page-header">
        <h1>Banner Management</h1>
        <button class="btn-primary" (click)="showForm = true" *ngIf="!showForm">+ Add Banner</button>
      </div>
      <div class="card form-card" *ngIf="showForm">
        <h2>{{ editingId ? 'Edit' : 'Add' }} Banner</h2>
        <form [formGroup]="form" (ngSubmit)="onSubmit()">
          <div class="form-group">
            <label>Title</label>
            <input type="text" formControlName="title" class="form-control">
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea formControlName="description" class="form-control" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>Image URL</label>
            <input type="text" formControlName="imageUrl" class="form-control">
          </div>
          <div class="form-group">
            <label>
              <input type="checkbox" formControlName="isActive"> Active
            </label>
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
              <th>Image URL</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let item of items">
              <td>{{ item.title }}</td>
              <td>{{ item.description }}</td>
              <td>{{ item.imageUrl }}</td>
              <td><span class="badge" [class.active]="item.isActive">{{ item.isActive ? 'Active' : 'Inactive' }}</span></td>
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
export class BannersComponent implements OnInit {
  items: Banner[] = [];
  showForm = false;
  form: FormGroup;
  editingId: string | null = null;

  constructor(private fb: FormBuilder, private service: BannerService) {
    this.form = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      imageUrl: ['', Validators.required],
      isActive: [true]
    });
  }

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.service.getAll().subscribe(data => this.items = data);
  }

  edit(item: Banner): void {
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
    this.form.reset({ isActive: true });
  }
}
