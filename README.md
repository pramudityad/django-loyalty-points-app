# Loyalty Points and Digital Payment System

This project is a backend API for a loyalty points system integrated with a simulated digital payment system. It is built with Django, Django REST Framework, Celery, and PostgreSQL, and it supports user management, points earning and redemption, simulated payment transactions, voucher management, data warehousing for transactions, background tasks for expiring points, and JWT-based authentication with role-based access control.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Running the Application Locally](#running-the-application-locally)
  - [Applying Migrations & Creating a Superuser](#applying-migrations--creating-a-superuser)
  - [Collecting Static Files](#collecting-static-files)
- [Running Unit Tests](#running-unit-tests)
- [Database and Data Warehouse Design](#database-and-data-warehouse-design)
- [Security Considerations](#security-considerations)
- [Additional Libraries and Rationale](#additional-libraries-and-rationale)
- [Final Notes](#final-notes)

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application Locally

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd django-loyalty-points-app
   ```

2. **Build and Start the Containers:**

   Use Docker Compose to build and start the following services:
   - **loyalty_web**: Django application running Gunicorn.
   - **loyalty_db**: PostgreSQL database.
   - **loyalty_redis**: Redis for Celery.
   - **loyalty_celery**: Celery worker for background tasks.
   - **loyalty_flower**: Flower for monitoring Celery.

   ```bash
   docker-compose up --build
   ```

3. **Apply Migrations & Create a Superuser:**

   Once the containers are running, apply the migrations:
   ```bash
   docker-compose exec loyalty_web python manage.py migrate
   ```
   Create a superuser (if desired) to access the Django admin:
   ```bash
   docker-compose exec loyalty_web python manage.py createsuperuser
   ```

4. **Collect Static Files:**

   To ensure that static files (e.g., for the Django admin) are served correctly, run:
   ```bash
   docker-compose exec loyalty_web python manage.py collectstatic --noinput
   ```

5. **Access the Application:**

   - **API/Homepage:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (if a default homepage is set up)
   - **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   - **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
   - **Flower (Celery Monitoring):** [http://127.0.0.1:5555/](http://127.0.0.1:5555/)

### Running Unit Tests

Unit tests are written using Pytest and pytest-django. To run the tests, execute:
```bash
docker-compose exec loyalty_web pytest
```

## Database and Data Warehouse Design

### Main Database
- **Purpose:** Stores operational data.
- **Key Models:** Users, Payment Transactions, Vouchers, and Points Configuration.
- **Data Types:**
  - **DecimalField:** Used for currency (e.g., `amount`, `points_balance`) to ensure precision.
  - **CharField:** For usernames, emails, and statuses.
- **Indexing:** PostgreSQL automatically indexes primary keys. Frequently queried fields (e.g., email, timestamp) can be indexed to improve performance.

### Data Warehouse
- **Purpose:** Stores copies of transaction data for reporting and analytics, separating analytical workloads from operational ones.
- **Design Considerations:** 
  - The warehouse database uses the same PostgreSQL engine.
  - Tables are structured to support business intelligence queries without impacting the performance of the operational database.

## Security Considerations

- **SQL Injection Prevention:**
  - Django's ORM automatically parameterizes queries, which helps mitigate SQL injection risks.
  
- **XSS Prevention:**
  - Django templates escape output by default.
  - Input data is validated via serializers and forms.

- **CSRF Protection:**
  - Django includes CSRF middleware for state-changing requests (POST, PUT, DELETE).
  - For APIs, JWT authentication minimizes session-based CSRF risks.

- **Authentication and Password Security:**
  - JWT (via djangorestframework-simplejwt) is used for secure, stateless authentication.
  - Django's built-in password hashing protects user credentials.

## Additional Libraries and Rationale

- **Django REST Framework (DRF):** Simplifies building RESTful APIs.
- **djangorestframework-simplejwt:** Implements JWT authentication for securing the API.
- **drf-yasg:** Generates Swagger/OpenAPI documentation automatically.
- **Celery:** Manages asynchronous background tasks (e.g., expiring points).
- **Redis:** Acts as the broker for Celery, providing fast in-memory operations.
- **Gunicorn:** A production-grade WSGI HTTP server for running Django.
- **WhiteNoise (if implemented):** Serves static files efficiently in production without a separate static file server.
- **pytest & pytest-django:** Provide robust testing frameworks to ensure high code quality.

## Final Notes

This project is designed to serve as a robust foundation for a loyalty points and digital payment system. The use of Docker Compose simplifies local development and deployment, ensuring consistency across environments. Feel free to customize and extend the application based on your specific needs.

Happy coding!
