import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse, HttpEvent} from '@angular/common/http';

import { Product } from '../models/product';
import { Observable, ObservableInput, catchError, delay, of, retry, retryWhen, shareReplay, timer } from 'rxjs';
import { ApiService } from './api.service';


@Injectable({
  providedIn: 'root'
})
export class ProductService {

  constructor(private http: HttpClient, private apiService: ApiService) {}

  // stream of product array of the server obtained by get call
  getProducts$ = this.http.get<Product[]>(this.apiService.getEndpointAPI() + "/product").pipe(
    // if no response try again 5 times
    retry(5)
  );

  /** return an observable of the product with the given id
   * 
   * @param idProduct id of the product to get
   * @returns observable of the product
   */
  getProduct(idProduct:number): Observable<Product> {
    return this.http.get<Product>(this.apiService.getEndpointAPI() + "/product/"+idProduct);
  }

  /** send to server a post request with the given data
   * 
   * @param form data to post
   * @returns an observable of the http event occuring 
   */
  postProduct<T>(form : FormData) : Observable<HttpEvent<T>> {
    return this.http.post<T>(this.apiService.getEndpointAPI()+"/version/sbom",form,{
      reportProgress: true,
      observe: 'events',
    });
    
    
    }
}
