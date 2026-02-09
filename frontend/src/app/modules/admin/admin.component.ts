import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AdminService } from '../../core/services/admin.service';
import { User } from '../../shared/models/models';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="page">
      <div class="page-header">
        <h1>User Management</h1>
        <button class="btn-primary" (click)="showForm = true" *ngIf="!showForm">+ Add User</button>
      </div>
      <div class="card form-card" *ngIf="showForm">
        <h2>{{ editingId ? 'Edit' : 'Add' }} User</h2>
        <form [formGroup]="form" (ngSubmit)="onSubmit()">
          <div class="form-row">
            <div class="form-group">
              <label>Name</label>
              <input type="text" formControlName="name" class="form-control">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" formControlName="email" class="form-control">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Password</label>
              <input type="password" formControlName="password" class="form-control">
            </div>
            <div class="form-group">
              <label>Role</label>
              <select formControlName="role" class="form-control">
                <option value="employee">Employee</option>
                <option value="admin">Admin</option>
                <option value="super_admin">Super Admin</option>
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
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let item of items">
              <td>{{ item.name }}</td>
              <td>{{ item.email }}</td>
              <td><span class="badge">{{ item.role.replace('_', ' ') }}</span></td>
              <td>{{ item.createdAt | date:'short' }}</td>
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
export class AdminComponent implements OnInit {
  items: User[] = [];
  showForm = false;
  form: FormGroup;
  editingId: string | null = null;

  constructor(private fb: FormBuilder, private service: AdminService) {
    this.form = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      role: ['employee', Validators.required]
    });
  }

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.service.getAllUsers().subscribe(data => this.items = data);
  }

  edit(item: User): void {
    this.showForm = true;
    this.editingId = item._id;
    this.form.patchValue(item);
    this.form.get('password')?.clearValidators();
  }

  delete(id: string): void {
    if (confirm('Are you sure?')) {
      this.service.deleteUser(id).subscribe(() => this.load());
    }
  }

  onSubmit(): void {
    if (this.form.valid) {
      const req = this.editingId
        ? this.service.updateUser(this.editingId, this.form.value)
        : this.service.createUser(this.form.value);
      req.subscribe(() => {
        this.load();
        this.showForm = false;
      });
    }
  }

  cancel(): void {
    this.showForm = false;
    this.form.reset({ role: 'employee' });
    this.form.get('password')?.setValidators(Validators.required);
  }
}
