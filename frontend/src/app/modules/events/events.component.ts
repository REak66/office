import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { EventService } from '../../core/services/event.service';
import { Event } from '../../shared/models/models';

@Component({
    selector: 'app-events',
    imports: [CommonModule, ReactiveFormsModule],
    template: `
    <div class="page">
      <div class="page-header">
        <h1>Event Management</h1>
        <button class="btn-primary" (click)="showForm = true" *ngIf="!showForm">+ Add Event</button>
      </div>
      <div class="card form-card" *ngIf="showForm">
        <h2>{{ editingId ? 'Edit' : 'Add' }} Event</h2>
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
              <label>Date</label>
              <input type="date" formControlName="date" class="form-control">
            </div>
            <div class="form-group">
              <label>Location</label>
              <input type="text" formControlName="location" class="form-control">
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
              <th>Date</th>
              <th>Location</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let item of items">
              <td>{{ item.title }}</td>
              <td>{{ item.description }}</td>
              <td>{{ item.date | date:'short' }}</td>
              <td>{{ item.location }}</td>
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
export class EventsComponent implements OnInit {
  items: Event[] = [];
  showForm = false;
  form: FormGroup;
  editingId: string | null = null;

  constructor(private fb: FormBuilder, private service: EventService) {
    this.form = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      date: ['', Validators.required],
      location: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.service.getAll().subscribe(data => this.items = data);
  }

  edit(item: Event): void {
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
