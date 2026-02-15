# Assumptions

- **Users**: The system is designed for internal staff rather than public-facing consumers.

- **Data Schema:**: Uploaded CSV files must contain Store ID, SKU, Product Name, Price, and Date. An optional Country Code field is supported.

- **Scalability & Performance**: To handle high-volume datasets (3,000 stores with millions of rows), the system utilizes chunked processing and batch database insertions to prevent memory overflows.

- **EData Persistence**: Users can modify existing records (e.g., updating prices or product names) post-load. Version history and audit trails are excluded from this initial MVP.

- **Deployment Environment**: For this POC, the application runs locally. PostgreSQL is containerized via Docker to ensure a clean environment without local dependencies. The architecture is designed to transition easily to managed services like AWS RDS for production.

- **Storage Strategy**: To keep the POC lightweight, raw CSV files are processed in-memory/streamed and are not persisted to long-term storage after processing.

- **Security**: Authentication and Authorization are currently out of scope for this version of the prototype.
