import { HttpClient, HttpEvent, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Analyse } from '../models/analyse';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class AnalyseService {

  constructor(private http: HttpClient, private apiService: ApiService) {}

  /** send to server a post request with the given data
   * 
   * @param form data to post
   * @returns an observable of the http event occuring 
   */
  postAnalyse<T>(form : any) : Observable<T> {
    return this.http.post<T>(this.apiService.getEndpointAPI()+"/analyse/new",form)
  }
  
  /** get from server the analyses of a version
   * 
   * @param idVersion the id of the version
   * @returns an observable of the analyses
   */
  getAnalyseByVersion(idVersion: number) : Observable<Analyse[]> {
    return this.http.get<Analyse[]>(this.apiService.getEndpointAPI()+"/analyse/version/"+idVersion)
  }

  /** get from server the analyses of a package
   * 
   * @param idPackage the id of the package
   * @returns an observable of the analyses
   */
  getAnalyseByPackage(idPackage: number) : Observable<Analyse[]> {
    return this.http.get<Analyse[]>(this.apiService.getEndpointAPI()+"/analyse/package/"+idPackage)
  }
  
  /** get from server the analyses of a vulnerabilty
   * 
   * @param idVulnerability the id of the vunerability
   * @returns an observable of the analyses
   */
  getAnalyseByVulnerability(idVulnerability: string) : Observable<Analyse[]> {
    return this.http.get<Analyse[]>(this.apiService.getEndpointAPI()+"/analyse/vulnerability/"+idVulnerability)
  }
  
  /** get from server the analyses of a vulnerabilty
   * 
   * @param idProduct the id of the product
   * @returns an observable of the analyses
   */
  getAnalyseByProduct(idProduct: number) : Observable<Analyse[]> {
    return this.http.get<Analyse[]>(this.apiService.getEndpointAPI()+"/analyse/product/"+idProduct)
  }

  /** send to server a delete request with the given data
   * 
   * @param form data to delete
   * @returns an observable of feed back of the operations done
   */
  deleteAnalyse<T>(form : any) : Observable<T> {
    const options = {
      headers: new HttpHeaders({'Content-Type': 'application/json'}),
      body: form,
    }
    return this.http.delete<T>(this.apiService.getEndpointAPI()+"/analyse/delete",options);
  }
}
