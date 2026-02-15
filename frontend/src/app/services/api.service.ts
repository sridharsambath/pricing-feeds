import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

const API = '/api';

export interface Product {
  id: number;
  store_id: string;
  sku: string;
  product_name: string;
  price: number;
  date: string;
  country_code: string;
}

export interface PaginationInfo {
  page: number;
  limit: number;
  total: number;
  has_more: boolean;
}

export interface ProductResponse {
  data: Product[];
  pagination: PaginationInfo;
}

export interface UploadResponse {
  accepted: number;
  rejected: number;
  total: number;
  errors: string[];
  upload_id: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  getProducts(page: number = 1, limit: number = 10, filters: any = {}): Observable<ProductResponse> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('limit', limit.toString());

    if (filters.store_id) {
      params = params.set('store_id', filters.store_id);
    }
    if (filters.sku) {
      params = params.set('sku', filters.sku);
    }
    if (filters.product_name) {
      params = params.set('product_name', filters.product_name);
    }
    if (filters.date_from) {
      params = params.set('date_from', filters.date_from);
    }
    if (filters.date_to) {
      params = params.set('date_to', filters.date_to);
    }
    if (filters.country_code) {
      params = params.set('country_code', filters.country_code);
    }

    return this.http.get<ProductResponse>(`${API}/products`, { params });
  }

  updateProduct(id: number, product: Partial<Product>): Observable<Product> {
    return this.http.patch<Product>(`${API}/products/${id}`, product);
  }

  uploadFile(file: File): Observable<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<UploadResponse>(`${API}/upload`, formData);
  }
}
