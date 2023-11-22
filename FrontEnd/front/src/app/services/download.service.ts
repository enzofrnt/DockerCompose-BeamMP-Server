import { HttpClient, HttpEvent, HttpEventType, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject, forkJoin, throwError } from 'rxjs';
import { catchError, filter, map, takeUntil, tap } from 'rxjs/operators';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class DownloadService {
  private downloadsProgress = new BehaviorSubject<Map<string, number>>(new Map())
  private cancelDownloads = new Subject<void>();

  constructor(private http: HttpClient, private apiService: ApiService) {}
  
  getCancelObservable() {
    return this.cancelDownloads.asObservable();
  }

  cancelAllDownloads() {
    this.cancelDownloads.next();
    this.resetProgress();
  }
  
  resetProgress() {
    this.downloadsProgress.next(new Map());
  }

  downloadFile(modName: string): Observable<Blob> {
    const url = `${this.apiService.getEndpointAPI()}/downmod/${modName}`;

    return this.http.get(url, { responseType: 'blob', reportProgress: true, observe: 'events' }).pipe(
      tap((event: HttpEvent<any>) => {
        if (event.type === HttpEventType.DownloadProgress) {
          const progress = event.total ? Math.round((100 * event.loaded) / event.total) : 0;
          this.updateProgress(modName, progress);
        }
      }),
      filter((event): event is HttpResponse<Blob> => event.type === HttpEventType.Response),
      map(event => {
        if (event.body) {
          return event.body;
        } else {
          // Gérer le cas où le corps est null
          throw new Error('Le fichier téléchargé est vide');
        }
      }),
      takeUntil(this.cancelDownloads),  // Annuler le téléchargement si un signal d'annulation est émis
      catchError(error => throwError(error))
    );
  }


  getDownloadsProgress(): Observable<number> {
    return this.downloadsProgress.asObservable().pipe(
      map(progressMap => {
        const progressValues = Array.from(progressMap.values());
        const totalProgress = progressValues.reduce((acc, progress) => acc + progress, 0);
        return progressValues.length ? totalProgress / progressValues.length : 0;
      })
    );
  }

  private updateProgress(modName: string, progress: number) {
    const currentProgressMap = this.downloadsProgress.value;
    currentProgressMap.set(modName, progress);
    this.downloadsProgress.next(currentProgressMap);
  }

  downloadMultipleFiles(modNames: string[]): Observable<any> {
    const downloadObservables = modNames.map(modName => this.downloadFile(modName));
    return forkJoin(downloadObservables);
  }
}
