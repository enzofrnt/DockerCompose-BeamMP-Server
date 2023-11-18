import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, retry } from 'rxjs';
import { Config } from '../models/config';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {

  constructor(private http: HttpClient, private apiService: ApiService) {}


  /** return an observable of the product with the given id
   * 
   * @param idProduct id of the product to get
   * @returns observable of the product
   */
  getConfig(): Observable<Config> {
    return this.http.get<Config>(this.apiService.getEndpointAPI() + "/config").pipe(
      retry(5)
    );
  }

}
