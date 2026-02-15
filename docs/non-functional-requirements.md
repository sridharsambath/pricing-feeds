# Non-Functional Requirements and How the Design Addresses Them

- **Scalability (3000 stores, multiple countries)**  
  - Stateless FastAPI so multiple instances can run behind a load balancer.  
  - Indexed queries (store_id, sku, date, country); pagination on all list endpoints.  
  - Pandas `read_csv(..., chunksize=...)` for large CSV uploads to avoid memory spikes.

- **Performance**  
  - DB indexes on filter columns; limit page size (e.g. 50–100 rows).  
  - No N+1 queries; single or batched DB calls per request. 

- **Security**  
  - parameterized queries to prevent SQL injection.  
  - Validate CSV content (types, ranges, row limits) and sanitize file names.

- **Maintainability**  
  - Clear split (frontend / backend); README with setup and run instructions.

- **Auditability**  
  - Store `created_at`/`updated_at` on records; `uploads` log (filename, storage_path, counts).  
  - Edit operations can log user and timestamp in DB.

- **Internationalization (multiple countries)**  
  - Backend stores dates in UTC
