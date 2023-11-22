import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { API_URL } from '../env';
import { Observable } from 'rxjs';
import { Mod } from '../models/mod';

@Injectable({
    providedIn: 'root'
  })
  export class ApiService {
    private conf: any;
  
    constructor(private http: HttpClient) {}
  
    loadConfig(): Promise<any> {
      return this.http.get('../../assets/json/runtime.json').toPromise().then(
        (config) => {
          this.conf = config;       
          console.log(this.conf);
          return this.conf; // Retourne la configuration chargée
        },
        (error) => {
          return Promise.reject(error);
        }
      );
    }
  
    getEndpointAPI(): string {
        console.log("API_URL: " + API_URL);
        if(this.conf?.API_URL==="$API_URL"){
            console.log("API_URL not set in runtime.json");
            return API_URL;
        } else {
            console.log("API_URL set in runtime.json");
            console.log(this.conf?.API_URL);
            return this.conf?.API_URL;
        }
    }

    getConfig(): Observable<any> {
        return this.http.get(this.getEndpointAPI() + '/config');
    }

    getServerConfig(): Observable<any> {
        return this.http.get(this.getEndpointAPI() + '/servconfig');
    }

    startServer(): Observable<any> {
        return this.http.get(this.getEndpointAPI() + '/start');
    }

    stopServer(): Observable<any> {
        return this.http.get(this.getEndpointAPI() + '/stop');
    }

    restartServer(): Observable<any> {
        return this.http.get(this.getEndpointAPI() + '/restart');
    }

    getServerStatus(): Observable<any> {
        return this.http.get(this.getEndpointAPI() + '/status');
    }

    getMods(): Observable<{[key: string]: Mod}> {
      return this.http.get<{[key: string]: Mod}>(`${this.getEndpointAPI()}/getmods`);
    }

    downloadMod(modName: string): Observable<Blob> {
      return this.http.get(`${this.getEndpointAPI()}/downmod/${modName}`, {
        responseType: 'blob'
      });
    }

    enableMod(modName: string): Observable<any> {
      return this.http.get(`${this.getEndpointAPI()}/enable/${modName ? modName.replace('.zip', '') : ''}`);
    }
  
    disableMod(modName: string): Observable<any> {
      return this.http.get(`${this.getEndpointAPI()}/disable/${modName ? modName.replace('.zip', '') : ''}`);
    }
  }