import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AttendanceService } from '../../core/services/attendance.service';
import { EmployeeService } from '../../core/services/employee.service';
import { Attendance, Employee } from '../../shared/models/models';

@Component({
  selector: 'app-attendance',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="page">
      <div class="page-header">
        <h1>Attendance Management</h1>
        <button class="btn-primary" (click)="showForm = true" *ngIf="!showForm">+ Add Attendance</button>
      </div>
      <div class="card form-card" *ngIf="showForm">
        <h2>{{ editingId ? 'Edit' : 'Add' }} Attendance</h2>
        <form [formGroup]="form" (ngSubmit)="onSubmit()">
          <div class="form-row">
            <div class="form-group">
              <label>Employee</label>
              <select formControlName="employeeId" class="form-control">
                <option value="">Select Employee</option>
                <option *ngFor="let emp of employees" [value]="emp._id">{{ emp.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Date</label>
              <input type="date" formControlName="date" class="form-control">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Clock In</label>
              <input type="time" formControlName="clockIn" class="form-control">
            </div>
            <div class="form-group">
              <label>Clock Out</label>
              <input type="time" formControlName="clockOut" class="form-control">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Location</label>
              <input type="text" formControlName="location" class="form-control">
            </div>
            <div class="form-group">
              <label>Type</label>
              <select formControlName="type" class="form-control">
                <option value="WFO">WFO</option>
                <option value="WFH">WFH</option>
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
              <th>Employee</th>
              <th>Date</th>
              <th>Clock In</th>
              <th>Clock Out</th>
              <th>Location</th>
              <th>Type</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let item of items">
              <td>{{ item.employeeId?.name || 'N/A' }}</td>
              <td>{{ item.date | date:'short' }}</td>
              <td>{{ item.clockIn }}</td>
              <td>{{ item.clockOut }}</td>
              <td>{{ item.location }}</td>
              <td><span class="badge">{{ item.type }}</span></td>
              <td class="actions">
                <button class="btn-icon" (click)="edit(item)">✏️</button>
                <button class="btn-icon" (click)="delete(item._id)">🗑️</button>
              </td>
            </tr>
            <tr *ngIf="items.length === 0"><td colspan="7" class="empty">No records found</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  `,
  styleUrls: ['../employees/employees.component.scss']
})
export class AttendanceComponent implements OnInit {
  items: Attendance[] = [];
  employees: Employee[] = [];
  showForm = false;
  form: FormGroup;
  editingId: string | null = null;

  constructor(
    private fb: FormBuilder,
    private service: AttendanceService,
    private employeeService: EmployeeService
  ) {
    this.form = this.fb.group({
      employeeId: ['', Validators.required],
      date: ['', Validators.required],
      clockIn: ['', Validators.required],
      clockOut: ['', Validators.required],
      location: ['', Validators.required],
      type: ['WFO', Validators.required]
    });
  }

  ngOnInit(): void {
    this.load();
    this.employeeService.getAll().subscribe(data => this.employees = data.employees || data);
  }

  load(): void {
    this.service.getAll().subscribe(data => this.items = data.attendance || data);
  }

  edit(item: Attendance): void {
    this.showForm = true;
    this.editingId = item._id;
    this.form.patchValue({
      ...item,
      employeeId: item.employeeId._id || item.employeeId,
      date: item.date ? new Date(item.date).toISOString().split('T')[0] : ''
    });
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
