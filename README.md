# Noorani Fabrics — Django E-Commerce Backend

A production-oriented **Django backend for a clothing and fashion e-commerce platform**, built to manage products, categories, shopping carts, customer orders, inventory, product images, and administrative operations.

The project provides a REST-style JSON API consumed by the storefront and includes a customized Django administration panel for managing the complete product and order lifecycle.

The application is deployed as a live web service and is continuously updated as the project evolves.

---

## 🚀 Project Overview

**Noorani Fabrics** is an online clothing store focused on showcasing and selling fashion products through a modern web storefront.

The backend is responsible for:

* Product and category management
* Product images and multiple product views
* Pricing and sale pricing
* Clothing sizes and stock
* Trending and featured products
* Shopping cart management
* Customer order creation
* Order item snapshots
* Order status management
* Inventory information
* Administrative product management
* Customer/order management
* JSON APIs for frontend integration
* Production database configuration
* Cloud-based media storage
* Static-file handling and production serving

The architecture separates the Django backend from the storefront/API consumption layer, allowing the frontend and backend to evolve independently.

---

## 🛠️ Technology Stack

### Backend

* **Python**
* **Django 6**
* Django ORM
* Django Admin
* JSON APIs
* PostgreSQL / SQLite
* Gunicorn

### Database

* PostgreSQL supported through `dj-database-url`
* SQLite available for local development

### Cloud & Deployment

* PythonAnywhere — live deployment
* Gunicorn
* WhiteNoise
* Environment-based configuration
* Cloudinary for media storage

### Frontend Integration

* HTML
* JavaScript
* JSON API
* CORS support

### Administration

* Django Admin
* Jazzmin Admin UI

---

## ✨ Main Features

### 🛍️ Product Management

Products are stored with detailed clothing-specific information including:

* Product name
* Category
* Current price
* Previous/discount price
* Product description
* Stock quantity
* Number sold
* Available sizes
* Product badges
* Trending status
* Featured status
* Creation timestamp

Each product can contain **up to five images**, allowing different views such as front, back, detail, and alternative product photography.

---

### 🗂️ Category Management

Products are organized through categories.

Each category includes:

* Name
* Unique slug
* Optional category image
* Related products

The admin dashboard also displays the number of products associated with each category.

---

### 🛒 Shopping Cart

The backend contains cart and cart-item models designed around session-based shopping.

Cart items can store:

* Product
* Quantity
* Size
* Color

This allows clothing-specific selections to be maintained as part of the customer's shopping session.

---

### 📦 Order Management

Customers can submit orders through the backend API.

An order stores:

* Customer first name
* Customer last name
* Email
* Phone number
* Delivery address
* Total price
* Payment method
* Order status
* Creation time
* Last update time

Orders have a generated identifier using the format:

```text
ORD-YYYY-000001
```

This provides a human-readable order reference for customers and administrators.

---

### 📋 Order Status Workflow

Orders support a complete operational workflow:

```text
Pending
   ↓
Confirmed
   ↓
Packed
   ↓
Shipped
   ↓
Delivered
```

Orders can also be marked as:

```text
Cancelled
```

This allows the admin team to track orders from initial placement through fulfillment.

---

### 🔐 Backend-Calculated Order Totals

The backend does not simply trust the total price submitted by the frontend.

When an order is created, the backend:

1. Receives the product IDs and quantities.
2. Retrieves the actual products from the database.
3. Uses the database price.
4. Calculates each item's cost.
5. Calculates the complete order total.
6. Stores the calculated total on the order.

This provides an important layer of protection against clients manipulating the order total.

---

### 🧾 Product Price Snapshots

`OrderItem` stores snapshots of:

* Product name
* Product price
* Quantity
* Size
* Color

This means historical orders can preserve the product information used when the order was placed, even if the product's current price or information changes later.

---

## 🔌 API Endpoints

The backend exposes lightweight JSON endpoints for frontend communication.

### Products

```http
GET /api/products/
```

Returns available products including:

* ID
* Name
* Category
* Price
* Previous price
* Images
* Sizes
* Stock
* Sales count
* Description
* Badge
* Trending status
* Featured status

---

### Categories

```http
GET /api/categories/
```

Returns product categories and their associated information.

---

### Create Order

```http
POST /api/orders/
```

Creates a new customer order.

Example request structure:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "03001234567",
  "address": "Customer delivery address",
  "payment_method": "Cash on Delivery",
  "items": [
    {
      "id": 1,
      "qty": 2,
      "size": "XL",
      "color": "Black"
    }
  ]
}
```

The backend validates the referenced products and calculates the order total from database prices.

A successful request returns an order reference such as:

```json
{
  "status": "success",
  "order_id": "ORD-2026-000001",
  "message": "We will contact you for confirmation"
}
```

---

## 🏗️ Architecture

The project follows a simple Django application architecture:

```text
                    ┌──────────────────────┐
                    │   Clothing Store UI  │
                    │   Web / Frontend     │
                    └──────────┬───────────┘
                               │
                               │ JSON API
                               ▼
                    ┌──────────────────────┐
                    │     Django Backend   │
                    │                      │
                    │   Product API        │
                    │   Category API       │
                    │   Order API          │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    │                      │
                    ▼                      ▼
             ┌──────────────┐       ┌──────────────┐
             │ PostgreSQL   │       │  Cloudinary  │
             │ / SQLite     │       │ Product      │
             │              │       │ Images       │
             └──────────────┘       └──────────────┘

                    ┌──────────────────────┐
                    │    Django Admin      │
                    │                      │
                    │ Products             │
                    │ Categories           │
                    │ Orders               │
                    │ Cart                 │
                    └──────────────────────┘
```

---

## 📁 Project Structure

```text
Shaban_cloth/
│
├── core/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── noorani_backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   └── index.html
│
├── media/
│   └── products/
│
├── manage.py
├── requirements.txt
├── build.sh
│
├── create_superuser.py
├── create_test_data.py
├── populate_db.py
├── add_demo_products.py
├── update_data.py
├── fix_images.py
└── fix_render.py
```

---

## 🧠 Django Data Model

The core application is organized around several main models:

```text
Category
   │
   └── Product
          │
          ├── CartItem
          │
          └── OrderItem
                    │
                    └── Order
```

### Category

Organizes clothing products into logical groups.

### Product

Represents an individual clothing item and stores pricing, inventory, images, sizes, descriptions, and merchandising flags.

### Cart

Represents a customer's shopping cart/session.

### CartItem

Connects products to carts while storing quantity, size, and color.

### Order

Stores customer information, delivery details, payment method, status, and calculated total.

### OrderItem

Stores the individual products purchased as part of an order together with historical product/price snapshots.

---

## 🖥️ Django Admin Dashboard

The project includes a customized **Jazzmin-powered Django Admin interface**.

Administrators can manage:

### Products

* Add products
* Edit prices
* Update stock
* Upload product images
* Assign categories
* Mark products as trending
* Mark products as featured
* Apply badges
* Search products
* Filter products

### Orders

* Search orders
* View customer information
* View ordered products
* Update order status
* View payment method
* View order totals
* Track order timestamps

### Categories

* Create categories
* Edit categories
* Generate slugs
* View product counts

This provides a centralized management system for the clothing store.

---

## ☁️ Media Storage

Product images use Django's image handling and are configured to support **Cloudinary-based storage**.

The project includes:

```text
cloudinary
django-cloudinary-storage
Pillow
```

This allows product photography to be stored separately from the application server and makes media management more suitable for a deployed application.

---

## 🗄️ Database Configuration

The project supports both local and production databases.

For local development, SQLite can be used:

```text
db.sqlite3
```

For production environments, the application can consume a database connection through:

```text
DATABASE_URL
```

The project uses `dj-database-url` to configure the Django database connection from environment variables.

PostgreSQL is supported through:

```text
psycopg2-binary
psycopg-binary
```

---

## ⚙️ Environment Variables

For production, sensitive configuration should be provided through environment variables rather than hardcoded values.

Example:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DATABASE_URL=your-database-url
```

If using Cloudinary:

```env
CLOUDINARY_URL=your-cloudinary-url
```

Never commit production secrets or credentials to GitHub.

---

## 💻 Local Development

### 1. Clone the repository

```bash
git clone https://github.com/Shabanali512/Shaban_cloth.git
cd Shaban_cloth
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin account

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

---

## 🚀 Production Deployment

The project includes a `build.sh` script that installs dependencies, collects static files, applies migrations, and prepares application data.

The deployment workflow includes:

```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

The live application is deployed on **PythonAnywhere**, where the Django application can be served through a production WSGI configuration.

The deployment setup is designed so that changes to the Django backend can be developed, committed to Git, and reflected in the live application deployment workflow.

---

## 🔄 Development & Live Updates

The project is actively developed through Git/GitHub.

Typical workflow:

```text
Code Change
     ↓
Local Testing
     ↓
Git Commit
     ↓
GitHub Push
     ↓
PythonAnywhere Deployment
     ↓
Live Application Updated
```

This makes it possible to continuously improve:

* Product functionality
* Backend APIs
* Database models
* Admin features
* Order processing
* Performance
* Deployment configuration

---

## 📦 Dependencies

The main project dependencies include:

```text
Django 6.0.4
django-cors-headers
django-jazzmin
Pillow
dj-database-url
psycopg2-binary
psycopg-binary
gunicorn
whitenoise
python-dotenv
cloudinary
django-cloudinary-storage
```

See `requirements.txt` for the complete pinned dependency list.

---

## 🔒 Security Considerations

The project uses several Django production features including:

* CSRF middleware
* Django authentication
* Password validation
* Security middleware
* Session middleware
* Environment-based secrets
* Production WSGI serving
* Static-file handling

For production deployment, `DEBUG` should be disabled and secrets should be supplied through environment variables.

---

## 🎯 Engineering Highlights

This project demonstrates practical experience with:

* Python backend development
* Django architecture
* Django ORM
* Database modeling
* REST-style JSON APIs
* E-commerce business logic
* Inventory management
* Shopping cart design
* Order processing
* Backend-side price calculation
* Product image management
* Cloud media storage
* PostgreSQL
* Production deployment
* Gunicorn
* WhiteNoise
* Environment-based configuration
* Django Admin customization
* Git/GitHub development workflow

---

## 📌 Future Improvements

Potential future improvements include:

* Django REST Framework
* JWT/user authentication
* Online payment integration
* Automated email/SMS order notifications
* Product reviews and ratings
* Advanced inventory tracking
* Coupon and discount management
* Order tracking for customers
* Redis caching
* Celery background tasks
* Automated testing and CI/CD
* API documentation with OpenAPI/Swagger
* More granular product variants for size/color inventory
* Production monitoring and logging

---

## 👨‍💻 Author

**Shaban Ali**

Backend / Cloud / DevOps Developer

GitHub:
https://github.com/Shabanali512

Repository:
https://github.com/Shabanali512/Shaban_cloth

---

## 📄 License

This project is intended as a personal/project portfolio application. Add an explicit license to the repository if you intend to permit reuse or redistribution.
