import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { environment } from '../environments/environment';
import { ChangeDetectorRef } from '@angular/core';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  uploadedFiles: string[] = [];
  files: File[] = [];
  isImage: boolean = false;
  currentPage: number = 1;
  pageSize: number = 10;
  totalPages: number = 0;
  displayedFiles: string[] = [];
  pages: number[] = [];

  constructor(
    private authService: AuthService,
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    console.log('Application initialized');
    if (!this.authService.checkAuthentication()) {
      console.log(`environment: ${environment.backendHost}`);
      this.promptForCredentials();
    } else {
      this.fetchUploadedFiles();
    }
  }

  promptForCredentials(): void {
    const username = window.prompt('Username:');
    const password = window.prompt('Password:');

    if (username === null || password === null) {
      console.log('Authentication cancelled');
      return;
    }

    if (!this.authService.login(username, password)) {
      console.log('Wrong credentials');
    } else {
      this.fetchUploadedFiles();
    }
  }

  changePage(page: number): void {
    if (page < 1 || page > this.totalPages) return;
    this.currentPage = page;
    this.fetchUploadedFiles();
  }

  onFileSelect(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files) return;
    this.files = Array.from(input.files);
    this.isImage = this.files.some((file) => file.type.startsWith('image/'));
  }

  onDragOver(event: Event): void {
    event.preventDefault();
  }

  onDragLeave(event: Event): void {
    // Logic for DragLeave-Event
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    if (event.dataTransfer && event.dataTransfer.files) {
      this.files = Array.from(event.dataTransfer.files);
      this.isImage = this.files.some((file) => file.type.startsWith('image/'));
    }
  }

  containsImageFile(): boolean {
    return this.files.some((file) => file.type.startsWith('image/'));
  }

  async deleteFile(fileName: string): Promise<void> {
    const apiUrl = `${environment.backendHost}/deletefile/${fileName}`;
    console.log(`Attempting to delete file: ${fileName}`);
    try {
      await firstValueFrom(this.http.delete(apiUrl));
      console.log(`File deleted: ${fileName}`);
      this.uploadedFiles = this.uploadedFiles.filter(
        (file) => file !== fileName
      );
      this.displayedFiles = this.displayedFiles.filter(
        (file) => file !== fileName
      );
      this.cdr.detectChanges();
    } catch (error) {
      console.error('Fehler beim Löschen', error);
    }
  }

  async fetchUploadedFiles(): Promise<void> {
    const apiUrl = `${environment.backendHost}/listfiles?page=${this.currentPage}&size=${this.pageSize}`;
    console.log(`Fetching uploaded files from: ${apiUrl}`);
    try {
      const response = await firstValueFrom(this.http.get<any>(apiUrl));
      console.log('Response:', response);

      if (response.files && response.files.length > 0) {
        this.uploadedFiles = response.files;
        this.displayedFiles = response.files;
        this.totalPages = response.total_pages;
        this.pages = Array.from({ length: this.totalPages }, (_, i) => i + 1);
        console.log(`Files fetched: ${this.uploadedFiles}`);
      } else {
        console.log('No files returned from the server.');
      }
    } catch (error) {
      console.error('Fehler beim Abrufen der Dateiliste', error);
    }
  }

  async uploadFiles(): Promise<void> {
    const formData = new FormData();
    for (const file of this.files) {
      formData.append('files', file, file.name);
    }

    const apiUrl = `${environment.backendHost}/uploadfiles`;
    console.log(`Uploading files to: ${apiUrl}`);

    try {
      await firstValueFrom(this.http.post(apiUrl, formData));
      console.log('Files uploaded successfully');
      await this.fetchUploadedFiles();
      this.files = [];
      this.cdr.detectChanges();
    } catch (error) {
      console.error('Fehler beim Hochladen', error);
    }
  }
}
