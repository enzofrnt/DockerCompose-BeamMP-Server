import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Version } from '../models/version';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class VersionService {

  constructor(private http: HttpClient, private apiService: ApiService) { }

  /** return an observable of the version with the given id
   * 
   * @param idVersion id of the version to get
   * @returns observable of the version
   */
  getVersion(idVersion:number): Observable<Version> {
    let a: ApiService = new ApiService(this.http);
    return this.http.get<Version>(this.apiService.getEndpointAPI() + "/version/"+idVersion);
  }
}
