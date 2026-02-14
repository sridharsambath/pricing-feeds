# pricing-feeds
Single-page web application for uploading, persisting, searching, and editing retail pricing feeds (CSV: Store ID, SKU, Product Name, Price, Date)

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Running the Application

Start the application with Docker Compose:

```bash
docker-compose up
```

This will start:
- **PostgreSQL Database** - Running on port 5433
- **Backend API** - Running on port 8000

The backend will automatically wait for the database to be healthy before starting.

### Configuration

#### Environment Setup

Create a `.env` file in the `backend` folder with the following content:

create manually:

```
DATABASE_URL=postgresql://admin:admin123@db:5432/pricing_feeds
```

The backend service reads configuration from `backend/.env` file for database connection and other environment variables.
