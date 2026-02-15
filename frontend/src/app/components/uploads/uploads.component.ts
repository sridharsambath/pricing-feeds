import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, UploadResponse } from '../../services/api.service';

@Component({
  selector: 'app-uploads',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './uploads.component.html',
  styleUrl: './uploads.component.css'
})
export class UploadsComponent {
  selectedFile: File | null = null;
  loading = false;
  successMessage: string | null = null;
  errorMessages: string[] = [];
  uploadStats: any = null;

  constructor(private apiService: ApiService) { }

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0] || null;
    this.successMessage = null;
    this.errorMessages = [];
    this.uploadStats = null;
  }

  uploadFile(): void {
    if (!this.selectedFile) {
      this.errorMessages = ['Please select a file first.'];
      return;
    }

    this.loading = true;
    this.successMessage = null;
    this.errorMessages = [];
    this.uploadStats = null;
    
    console.log('Uploading file:', this.selectedFile.name);

    this.apiService.uploadFile(this.selectedFile).subscribe({
      next: (response: UploadResponse) => {
        console.log('File upload response:', response);
        
        if (response.errors && response.errors.length > 0) {
          this.errorMessages = response.errors;
        } else {
          this.successMessage = "File uploaded successfully!";
          this.selectedFile = null;
          // Reset file input
          const fileInput = document.getElementById('file-input') as HTMLInputElement;
          if (fileInput) fileInput.value = '';
        }
        
        this.uploadStats = {
          accepted: response.accepted,
          rejected: response.rejected,
          total: response.total
        };
        this.loading = false;
      },
      error: (err) => {
        console.error('Error uploading file:', err);
        
        if (err.error?.errors) {
          this.errorMessages = err.error.errors;
        } else if (err.error?.detail) {
          this.errorMessages = [err.error.detail];
        } else {
          this.errorMessages = ['Failed to upload file.'];
        }
        
        this.loading = false;
      }
    });
  }
}

