# Omni-Data

A multi-tenant merchant analytics and transaction management platform for fintech applications.

## The Problem

Merchants need centralized visibility into transaction data, detailed analytics, and the ability to export reports, while operating in a secure, isolated multi-tenant environment.

## What It Solves

- **Multi-tenant data isolation** – Secure separation between merchants using tenant-aware middleware
- **Transaction analytics** – Real-time dashboards and performance metrics
- **Async exports** – Background job processing for large data exports (CSV format)
- **Rate limiting & security** – Built-in throttling and performance monitoring

## Key Features

- Merchant dashboard with transaction filtering and search
- Analytics summary endpoints with pagination
- Asynchronous CSV export with status tracking
- Multi-merchant support with header-based tenant routing
- Performance metrics middleware for slow query detection

## Tech Stack

**Backend:** Django, Django REST Framework  
**Database:** PostgreSQL (Supabase integration)  
**Frontend:** React, Axios  
**Deployment:** Docker (separate containers for frontend/backend)  
**CI/CD:** Github Actions


## Good Practices

- **Tenant isolation** via middleware with thread-local context
- **Async processing** for non-blocking exports
- **Pagination & throttling** to manage load
- **Error handling** with 404 detection for cross-tenant requests
- **Environment-based config** using `.env` files
- **Containerized deployment** for consistency

## Getting Started

```bash
# Backend
docker build -f Dockerfile.backend -t omni-data-backend .
docker run -p 8000:8000 omni-data-backend

# Frontend
docker build -f Dockerfile.frontend -t omni-data-frontend .
docker run -p 3000:3000 omni-data-frontend
