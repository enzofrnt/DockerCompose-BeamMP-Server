import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { forkJoin } from 'rxjs';

import { ApiService } from '../services/api.service';
import { DownloadService } from '../services/download.service';
import { DownloadDialogComponent } from './download-dialog/download-dialog.component';
import { Mod } from '../models/mod';

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss']
})
export class FormComponent implements OnInit {
  mods: Mod[] = [];
  selectedMods: Set<string> = new Set();

  constructor(
    private apiService: ApiService, 
    private downloadService: DownloadService,
    private dialog: MatDialog
  ) {}

  ngOnInit() {
    this.apiService.getMods().subscribe(data => {
      this.mods = Object.keys(data).map(key => ({ name: key, path: data[key].path, enable: data[key].enable , isSelected: false }));
    });
  }

  toggleModSelection(modName: string) {
    this.mods = this.mods.map(mod => {
      if (mod.name === modName && mod.enable) {
        if (mod.isSelected) {
          this.selectedMods.delete(modName);
        } else {
          this.selectedMods.add(modName);
        }
        return { ...mod, isSelected: !mod.isSelected };
      }
      return mod;
    });
  }

  selectAllMods(event: any) {
    const isChecked = event.target.checked;
    this.mods = this.mods.map(mod => {
      if (mod.enable) {
        if (isChecked) {
          this.selectedMods.add(mod.name);
        } else {
          this.selectedMods.delete(mod.name);
        }
        return { ...mod, isSelected: isChecked };
      }
      return mod;
    });
  }

  downloadSelectedMods() {
    this.downloadService.resetProgress();
  
    if (this.selectedMods.size === 0) {
      // Afficher un message d'erreur ou une notification si aucun mod n'est sélectionné
      return;
    }
  
    const dialogRef = this.dialog.open(DownloadDialogComponent, {
      data: { progress: this.downloadService.getDownloadsProgress() },
      panelClass: 'download-dialog'
    });
  
    dialogRef.afterClosed().subscribe(() => {
      this.downloadService.cancelAllDownloads();
    });
  
    const downloadObservables = Array.from(this.selectedMods).map(modName => {
      return this.downloadService.downloadFile(modName);
    });
  
    forkJoin(downloadObservables).subscribe({
      next: (blobs) => {
        blobs.forEach((blob, index) => {
          const modName = Array.from(this.selectedMods)[index];
          this.saveFile(blob, modName);
        });
        dialogRef.close();
      },
      error: (error) => {
        dialogRef.close();
      }
    });
  }
  
  private saveFile(blob: Blob, fileName: string) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    a.click();
    window.URL.revokeObjectURL(url);
  }

  changeModStatus(mod: Mod) {
    if (mod.enable) {
      this.apiService.disableMod(mod.name).subscribe(() => {
        mod.enable = false; 
        mod.isSelected = false;
      });
    } else {
      this.apiService.enableMod(mod.name).subscribe(() => {
        mod.enable = true;
      });
    }
  }
}
