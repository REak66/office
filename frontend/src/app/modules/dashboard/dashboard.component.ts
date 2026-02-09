import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration } from 'chart.js';
import { DashboardService } from '../../core/services/dashboard.service';
import { AttendanceService } from '../../core/services/attendance.service';
import { CircularService } from '../../core/services/circular.service';
import { DashboardSummary, Attendance, CircularLetter } from '../../shared/models/models';

@Component({
    selector: 'app-dashboard',
    imports: [CommonModule, BaseChartDirective],
    templateUrl: './dashboard.component.html',
    styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  summary: DashboardSummary | null = null;
  attendanceList: Attendance[] = [];
  circularList: CircularLetter[] = [];

  lineChartData: ChartConfiguration<'line'>['data'] = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        data: [65, 59, 80, 81, 56, 55],
        label: 'Present',
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4
      },
      {
        data: [28, 48, 40, 19, 86, 27],
        label: 'Absent',
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  };

  lineChartOptions: ChartConfiguration<'line'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  doughnutChartData: ChartConfiguration<'doughnut'>['data'] = {
    labels: ['Awaiting Validation', 'Awaiting Verification', 'Completed', 'Closed'],
    datasets: [
      {
        data: [30, 25, 35, 10],
        backgroundColor: ['#3b82f6', '#f59e0b', '#10b981', '#6366f1']
      }
    ]
  };

  doughnutChartOptions: ChartConfiguration<'doughnut'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom'
      }
    }
  };

  constructor(
    private dashboardService: DashboardService,
    private attendanceService: AttendanceService,
    private circularService: CircularService
  ) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.dashboardService.getSummary().subscribe({
      next: (data) => {
        this.summary = data;
      },
      error: (err) => console.error('Error loading summary:', err)
    });

    this.dashboardService.getAttendanceSummary().subscribe({
      next: (data) => {
        this.lineChartData.labels = data.map(d => d.month);
        this.lineChartData.datasets[0].data = data.map(d => d.present);
        this.lineChartData.datasets[1].data = data.map(d => d.absent);
      },
      error: (err) => console.error('Error loading attendance summary:', err)
    });

    this.dashboardService.getDocumentSubmission().subscribe({
      next: (data) => {
        this.doughnutChartData.labels = data.breakdown.map(d => d.status);
        this.doughnutChartData.datasets[0].data = data.breakdown.map(d => d.count);
      },
      error: (err) => console.error('Error loading document submission:', err)
    });

    this.attendanceService.getAll().subscribe({
      next: (data) => {
        this.attendanceList = data.slice(0, 5);
      },
      error: (err) => console.error('Error loading attendance:', err)
    });

    this.circularService.getAll().subscribe({
      next: (data) => {
        this.circularList = data.slice(0, 5);
      },
      error: (err) => console.error('Error loading circulars:', err)
    });
  }

  getPriorityClass(priority: string): string {
    const classes: any = {
      'very_urgent': 'priority-very-urgent',
      'urgent': 'priority-urgent',
      'normal': 'priority-normal'
    };
    return classes[priority] || 'priority-normal';
  }
}
