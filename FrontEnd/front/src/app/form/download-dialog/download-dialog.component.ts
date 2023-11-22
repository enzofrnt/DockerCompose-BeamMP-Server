import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { DownloadService } from '../../services/download.service';

@Component({
  selector: 'app-download-dialog',
  templateUrl: './download-dialog.component.html',
  styleUrls: ['./download-dialog.component.scss']
})
export class DownloadDialogComponent {
  progressValue: number = 0;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<DownloadDialogComponent>,
    private downloadService: DownloadService
  ) {
    this.data.progress.subscribe((progress: number) => {
      this.progressValue = progress;
    });
  }

  cancelDownloads() {
    this.downloadService.cancelAllDownloads();
    this.dialogRef.close();
  }
}