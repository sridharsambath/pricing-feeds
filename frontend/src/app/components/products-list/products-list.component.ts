import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, Product, ProductResponse } from '../../services/api.service';

@Component({
  selector: 'app-products-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './products-list.component.html',
  styleUrl: './products-list.component.css'
})
export class ProductsListComponent implements OnInit {
  products: Product[] = [];
  loading = false;
  error: string | null = null;
  
  // Pagination
  currentPage = 1;
  pageSize = 10;
  totalItems = 0;
  hasMore = false;
  
  productFilters = {
    product_name: '',
    store_id: '',
    sku: '',
    country_code: '',
    date_from: '',
    date_to: ''
  };

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.loading = true;
    this.error = null;
    console.log('Loading products with filters:', this.productFilters);
    
    this.apiService.getProducts(this.currentPage, this.pageSize, this.productFilters)
      .subscribe({
        next: (response: ProductResponse) => {
          this.products = response.data;
          this.totalItems = response.pagination.total;
          this.hasMore = response.pagination.has_more;
          this.loading = false;
          console.log(`Loaded ${this.products.length} products`);
        },
        error: (err) => {
          console.error('Error loading products:', err);
          this.error = 'Failed to load products. Try again.';
          this.loading = false;
        }
      });
  }

  onSearch(): void {
    this.currentPage = 1;
    this.loadProducts();
  }

  onClearFilters(): void {
    this.productFilters = {
      product_name: '',
      store_id: '',
      sku: '',
      country_code: '',
      date_from: '',
      date_to: ''
    };
    this.currentPage = 1;
    this.loadProducts();
  }

  nextPage(): void {
    if (this.hasMore) {
      this.currentPage++;
      this.loadProducts();
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.loadProducts();
    }
  }

  goToPage(page: number): void {
    this.currentPage = page;
    this.loadProducts();
  }

  get totalPages(): number {
    return Math.ceil(this.totalItems / this.pageSize);
  }

  get startItem(): number {
    return (this.currentPage - 1) * this.pageSize + 1;
  }

  get endItem(): number {
    return Math.min(this.currentPage * this.pageSize, this.totalItems);
  }
}
