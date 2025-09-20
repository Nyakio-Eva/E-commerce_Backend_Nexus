# E-commerce_Backend_Nexus


## Overview
This project simulates a **real-world e-commerce backend**, designed with a focus on **scalability, security, and performance**.  
It provides APIs to manage products, categories, and users, while ensuring efficient data retrieval through **filtering, sorting, and pagination**.  

The backend demonstrates how backend engineers can design, optimize, and document APIs in a production-like environment.

---

## Project Goals
- **CRUD APIs**: Implement create, read, update, and delete operations for products, categories, and users.  
- **Filtering, Sorting, Pagination**: Support efficient product discovery with dynamic queries.  
- **Database Optimization**: Design relational schemas and apply indexing/query optimization for better performance.  
- **Authentication & Security**: Provide secure user authentication and role-based access using **JWT**.  
- **API Documentation**: Generate and publish API documentation for seamless frontend integration.

---

## Technologies Used
- **[Django](https://www.djangoproject.com/)** – High-level Python web framework for scalable backend development.  
- **[PostgreSQL](https://www.postgresql.org/)** – Robust relational database with strong query optimization.  
- **[JWT](https://jwt.io/)** – JSON Web Tokens for secure user authentication and authorization.  
- **Swagger/OpenAPI** – Interactive API documentation and testing.

---

## Key Features
### 1. CRUD Operations
- Manage **Products** and **Categories** via RESTful APIs.  
- User authentication and account management using **JWT**.  

### 2. API Features
- **Filtering & Sorting**: Filter products by category, price, stock status. 
- **Pagination**: Efficiently handle large product datasets with paginated responses.  

### 3. API Documentation
- Swagger/OpenAPI integrated for live API testing.  
- Postman collections for external testing and frontend integration.  

---
API Endpoints

### 1. User Authentication
#### Register
POST /api/users/register/

#### Login
POST /api/users/login/

#### Get Profile
GET /api/users/me/

#### Update Profile
PATCH /api/users/me/

#### Change Password
POST /api/users/change-password/

#### Password Reset
POST /api/users/reset-password/

### 2. Products
#### Create Product
POST /api/products/

#### List Products (with filtering, sorting, pagination)
GET /api/products/?category=category_id&sort=sort_field&page=page_number&page_size=page_size

#### Update Product
PUT /api/products/{product_id}/

#### Partial Update Product
PATCH /api/products/{product_id}/

#### Delete Product
DELETE /api/products/{product_id}/

### 3. Categories
#### Create Category
POST /api/categories/

