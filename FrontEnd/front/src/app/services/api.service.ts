import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { API_URL } from '../env';

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
  }