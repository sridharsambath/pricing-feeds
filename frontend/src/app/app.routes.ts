import { Routes } from '@angular/router';

export const routes: Routes = [
    {path: '', loadComponent: () => import('./components/uploads/uploads.component').then(m => m.UploadsComponent)},
    {path: 'products-list', loadComponent: () => import('./components/products-list/products-list.component').then(m => m.ProductsListComponent)},
];
