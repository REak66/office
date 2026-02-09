import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CircularService } from '../../core/services/circular.service';
import { CircularLetter } from '../../shared/models/models';

@Component({
  selector: 'app-circular',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="page">
      <div class="page-header">
        <h1>Circular Letters</h1>
        <button class="btn-primary" (click)="showForm = true" *ngIf="!showForm">+ Add Circular</button>
      </div>
      <div class="card form-card" *ngIf="showForm">
        <h2>{{ editingId ? 'Edit' : 'Add' }} Circular Letter</h2>
        <form [formGroup]="form" (ngSubmit)="onSubmit()">
          <div class="form-row">
            <div class="form-group">
              <label>Title</label>
              <input type="text" formControlName="title" class="form-control">
            </div>
            <div class="form-group">
              <label>Reference Number</label>
              <input type="text" formControlName="referenceNumber" class="form-control">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Date</label>
              <input type="date" formControlName="date" class="form-control">
            </div>
            <div class="form-group">
              <label>Priority</label>
              <select formControlName="priority" class="form-control">
                <option value="normal">Normal</option>
                <option value="urgent">Urgent</option>
                <option value="very_urgent">Very Urgent</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Content</label>
            <textarea formControlName="content" class="form-control" rows="5"></textarea>
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
              <th>Reference</th>
              <th>Date</th>
              <th>Priority</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let item of items">
              <td>{{ item.title }}</td>
              <td>{{ item.referenceNumber }}</td>
              <td>{{ item.date | date:'short' }}</td>
              <td><span class="badge">{{ item.priority.replace('_', ' ') }}</span></td>
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
export class CircularComponent implements OnInit {
  items: CircularLetter[] = [];
  showForm = false;
  form: FormGroup;
  editingId: string | null = null;

  constructor(private fb: FormBuilder, private service: CircularService) {
    this.form = this.fb.group({
      title: ['', Validators.required],
      referenceNumber: ['', Validators.required],
      date: ['', Validators.required],
      priority: ['normal', Validators.required],
      content: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.service.getAll().subscribe(data => this.items = data);
  }

  edit(item: CircularLetter): void {
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
    this.form.reset({ priority: 'normal' });
  }
}
