# E-commerce_Backend_Nexus


## Overview
This project simulates a **real-world e-commerce backend**, designed with a focus on **scalability, security, and performance**.  
It provides APIs to manage products, categories, and users, while ensuring efficient data retrieval through **filtering, sorting, and pagination**.  

The backend demonstrates how backend engineers can design, optimize, and document APIs in a production-like environment.

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
- **[PostgreSQL](https://www.postgresql.org/)** – Robust relational database with strong query optimization.  
- **[JWT](https://jwt.io/)** – JSON Web Tokens for secure user authentication and authorization.  
- **Swagger/OpenAPI** – Interactive API documentation and testing.
 

---
## API Endpoints

### 1. User Authentication
POST /api/users/register/ - Register

POST /api/users/login/ - login
 
GET /api/users/me/ - Get Profile

PATCH /api/users/me/ - Update Profile

POST /api/users/change-password/ - Change Password

POST /api/users/reset-password/ - Password Reset

### 2. Products
POST /api/products/ -  Create Product

GET /api/products/?category=category_id&ordering=sort_field&page=page_number&page_size=page_size - List Products (with filtering, sorting, pagination)

PUT /api/products/{product_id}/ - Update Product

PATCH /api/products/{product_id}/ - Partial Update Product

DELETE /api/products/{product_id}/ - Delete Product

### 3. Categories
POST /api/categories/ - create category (admin only)

PUT /api/categories/{category_id}- Update category

DELETE /api/categories/{category_id} - Delete category

### 4. Shopping Cart
GET /api/cart/ → Get user’s shopping cart

POST /api/cart/ → Add item to cart

PATCH /api/cart/items/{item_id}/ → Update cart item (e.g., quantity)

POST /api/cart/items/{item_id}/move-to-favorites/ → add item to favorites

DELETE /api/cart/items/{item_id}/ → Remove item from cart

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

 

## Entity Relationship Diagram and Flowchart

- Link to  the  → **[ERD](https://dbdiagram.io/d/Geocel-Enterprises-ERD-666c20c6a179551be6e449bf)**
- Link to the  → **[FlowChart for processes](https://excalidraw.com/#json=L8IIOeAZwBUv1s2RahAJ0,nmx8XTwIhszSTSpf8G2-RA)**

