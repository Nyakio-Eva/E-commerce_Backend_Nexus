# E-commerce_Backend_Nexus

## Overview
TThe E-commerce Backend Nexus is a production-ready backend API that powers a modern e-commerce system.
It is designed with a strong emphasis on scalability, security, and performance.

The system provides features such as user authentication, product/catalog management, shopping carts, wishlists, orders, payments, and reviews, all accessible via well-documented RESTful APIs.

It also comes with interactive API documentation via Swagger for live testing.

---
## Main Functionalities
### 1. CRUD APIs

#### Features:

* Create, read, update, and delete operations for products, categories, and users.

* Role-based restrictions (e.g., only admins can create/update/delete products).

* Standardized RESTful endpoints for consistency.

#### Benefits:

* Ensures flexibility in managing catalog and users.

* Keeps data up-to-date with minimal effort.

* Provides a strong foundation for frontend apps (web or mobile) to consume data seamlessly.

### 2. Filtering, Sorting, Pagination

#### Features:

* Filter products by category, price range, availability.

* Sort products by price, name, or newest.

* Paginated responses for large datasets.

#### Benefits:

* Enhances user experience with faster product discovery.

* Reduces server load by avoiding unnecessary large payloads.

* Ensures scalability for growing product catalogs.

### 3. Database Optimization

#### Features:

* Well-structured relational schema with proper indexes.

* Query optimization with select_related and prefetch_related.

* Caching frequently accessed queries.

#### Benefits:

* High performance even with thousands of products.

* Reduces query execution time, leading to faster API responses.

* Ensures smooth scalability as traffic grows.

### 4. Authentication & Security (JWT)

#### Features:

* Secure user registration & login with JWT tokens.

* Role-based access (e.g customer vs. admin).

* Token expiration and refresh mechanism.

#### Benefits:

* Protects sensitive endpoints from unauthorized access.

* Provides a safe shopping environment for users.

* Ensures compliance with modern security standards.

### 5. API Documentation (Swagger / OpenAPI)

#### Features:

* Auto-generated interactive API documentation.

* Live testing of endpoints directly from Swagger UI.

* Postman collection export for external testing.

#### Benefits:

* Simplifies frontend-backend collaboration.

* Ensures APIs are discoverable and easy to use.

* Speeds up onboarding for new developers.

### 6. Payment Integration (M-Pesa, PayPal, Visa)

#### Features:

* Support for multiple payment gateways (M-Pesa, PayPal, Visa).

* Secure payment initiation and verification endpoints.

* Transaction history tracking.

#### Benefits:

* Provides payment flexibility to customers.

* Builds trust with secure payment handling.

* Expands market reach by supporting global & local payment methods.

---

## Technologies Used
- **[Django](https://www.djangoproject.com/)** – High-level Python web framework for scalable backend development.  
- **[Django REST Framework (DRF)](https://www.django-rest-framework.org/)** - A powerful and flexible toolkit for building Web APIs.
- **[PostgreSQL](https://www.postgresql.org/)** – Robust relational database with strong query optimization.  
- **[JWT](https://jwt.io/)** – JSON Web Tokens for secure user authentication and authorization.  
- **Swagger/OpenAPI** – Interactive API documentation and testing.
 

---
## Getting Started (Local Setup)

    1. Clone the Repository
        git clone https://github.com/Nyakio-Eva/ecommerce-backend-nexus.git
        cd ecommerce-backend-nexus

    2. Create and Activate Virtual Environment
        python -m venv venv
        source venv/bin/activate   # For Linux/Mac
        venv\Scripts\activate      # For Windows

    3. Install Dependencies
        pip install -r requirements.txt

    4. Configure Database
        Update your .env file with PostgreSQL credentials:

        DATABASE_URL=postgres://user:password@localhost:5432/ecommerce_db
        SECRET_KEY=your_secret_key
        DEBUG=True

    5. Run Migrations
        python manage.py migrate

    6. Create Superuser
       python manage.py createsuperuser

    7. Start Development Server
        python manage.py runserver

## API Documentation & Testing
🔹 Swagger (Hosted)

You can test the API live via Swagger UI at:
👉 https://e-commerce-backend-nexus-api.onrender.com

Here you can:

- Authenticate using JWT tokens (Authorize button at the top right).

- Test endpoints directly from the browser.

- Explore request/response formats.


## API Endpoints
### Authentication

POST /api/users/register/ – Register

POST /api/users/login/ – Login

GET /api/users/me/ – Get profile

PATCH /api/users/me/ – Update profile

POST /api/users/change-password/ – Change password

POST /api/users/reset-password/ – Reset password

### Products

GET /api/products/ – List products (with filtering, sorting, pagination)

POST /api/products/ – Create product (admin)

PUT /api/products/{id}/ – Update product

DELETE /api/products/{id}/ – Delete product

### 3. Categories 
POST /api/categories/ - create category (admin only) 
PUT /api/categories/{category_id}- Update category 
DELETE /api/categories/{category_id} - Delete category 

### 4. Shopping Cart 
GET /api/cart/ → Get user’s shopping cart 
POST /api/cart/ → Add item to cart 
PATCH /api/cart/items/{item_id}/ → Update cart item (e.g., quantity) 
POST /api/cart/items/{item_id}/move-to-favorites/ → add item to favorites DELETE /api/cart/items/{item_id}/ → Remove item from cart 
DELETE /api/cart/clear/ → Clear the entire cart 

### 5. Wishlist 
GET /api/favorites/ → Get all favorite items 
POST /api/favorites/add/ → Add product to favorites 
DELETE /api/favorites/{product_id}/ → Remove product from favorites 

### 6. Orders & Checkout 
POST /api/orders/checkout/ → Convert cart into an order 
GET /api/orders/ → Get all orders for logged-in user 
GET /api/orders/{order_id}/ → Get single order details 
PATCH /api/orders/{order_id}/status/ → Update order status (admin only) 

### 7. Payments 
POST /api/payments/initiate/ → Initiate payment (Stripe/PayPal/m-pesa integration) 
POST /api/payments/verify/ → Verify payment transaction 
GET /api/payments/history/ → List user’s payment history 

### 8. Reviews & Ratings 
POST /api/products/{product_id}/reviews/ → Add review for a product 
GET /api/products/{product_id}/reviews/ → Get product reviews 
PATCH /api/reviews/{review_id}/ → Update review 
DELETE /api/reviews/{review_id}/ → Delete review 

### 9.Admin 
GET /api/users/admin/dashboard/ → Sales summary, order counts, etc. 
GET /api/users/admin/users/ → Manage users 
GET /api/users/admin/orders/ → Manage all orders 
GET /api/users/admin/products/low-stock/ → Inventory alerts

## Database & Process Flows

- Link to the → **[ERD](https://dbdiagram.io/d/Geocel-Enterprises-ERD-666c20c6a179551be6e449bf)** 
- Link to the → **[FlowChart for processes](https://excalidraw.com/#json=L8IIOeAZwBUv1s2RahAJ0,nmx8XTwIhszSTSpf8G2-RA)**

## Contribution

Contributions are welcome!

    Fork the repo

    Create a new branch (feature/new-feature)

    Commit changes

    Open a Pull Request

## License

This project is licensed under the MIT License – free to use and modify.