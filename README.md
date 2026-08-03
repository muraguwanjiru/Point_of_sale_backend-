# Retail Point of Sale (POS) Application
> **Database Schema & API Documentation**

This repository contains the comprehensive database schema design and backend implementation for a retail Point of Sale (POS) application built using **FastAPI**. 

The system is tailored for small-to-medium retail businesses such as grocery stores, apparel shops, and specialty boutique retailers.

---

## 🚀 Main System Features

*   **Inventory & Product Management**
    *   Organize merchandise cleanly by product categories.
    *   Seamlessly track stock levels provided by suppliers.
*   **Sales & Checkout Processing**
    *   Perform lightning-fast checkout workflows.
    *   Calculate discounts and capture real-time line-item details.
*   **Flexible Payments**
    *   Support diverse, split-tender transaction workflows.
    *   Accept cash, credit cards, and digital/mobile wallets.
*   **Customer & User Management**
    *   Track customer purchase histories for loyalty rewards.
    *   Secure employee access via role-based user permissions (RBAC).
*   **Compliance & Auditing**
    *   Automatically generate deterministic, immutable physical receipts for every successful sale.

---

## 📊 Entity Relationship Diagram (ERD)

The visual database architecture and ERD can be accessed via the link below

**Link to ERD diagram**
https://lucid.app/lucidchart/bc01eb06-894e-4be1-a14f-580ce6f72dbb/edit?viewport_loc=-1724%2C-764%2C3963%2C2171%2C0_0&invitationId=inv_3dc473fb-102a-4d98-8ee6-066f6722da65



## 🔗 Relational Rules & Cardinality

The core database architecture relies on the following strategic constraints and rules:

*   **Category --> Product** *(One-to-Many)*
    *   A category groups numerous items, while a given product resolves to exactly one classification group.
*   **Supplier --> Product** *(One-to-Many)*
    *   A wholesale supplier feeds multiple catalog listings; a product maps back to its primary sourcing entity.
*   **Customer --> Sale** *(One-to-Many)*
    *   Registered customers can checkout repeatedly over time. Walk-in guests generate anonymous checkout logs (nullable customer fields).
*   **User --> Sale** *(One-to-Many)*
    *   Store employees ring up endless distinct sales events during their active system service history.
*   **Sale --> Sale Item** *(One-to-Many)*
    *   An absolute receipt header references one or more item line items within the checkout basket.
*   **Product --> Sale Item** *(One-to-Many)*
    *   Products populate multiple invoice rows over time while an isolated row references one fixed product model.
*   **Sale --> Payment** *(One-to-Many)*
    *   Bill totals can be settled over multi-tender actions (e.g., splitting balances across cash and card combinations).
*   **Sale --> Receipt** *(One-to-One)*
    *   Successful sales map directly to exactly one legal, customer-facing checkout invoice printout.

---

## 🔌 Database Connectivity & Configuration

The application leverages **SQLAlchemy** (Object-Relational Mapper) paired with the **asyncpg** driver to establish asynchronous connections to a **PostgreSQL** database cluster.

### Setup & Integration
1. **Environment Variables**: Core connection strings and credential strings are decoupled from the application logic and loaded dynamically using a `.env` configuration file:
   ```env
   DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>:<port>/<database_name>
   ```
2. **Engine Initialization**: An asynchronous database engine instance is created via `create_async_engine()`, handling connection pooling configurations automatically to manage high-concurrency client requests cleanly.
3. **Session Management**: Database handshakes are isolated using a context-managed `async_sessionmaker`. FastAPI routes dependency inject these sessions through a reusable utility function (`get_db`), ensuring that every incoming API call opens a clean connection transaction and terminates it safely upon response delivery.


## 🛠️ API Testing with Swagger UI

The FastAPI backend includes an interactive, browser-based API documentation page via **Swagger UI**. This was used to thoroughly test all database endpoints and relationship constraints without needing external API clients.

### How to Access and Test:
1. **Start the Server**: Run the FastAPI application locally (e.g., using `uvicorn main:app --reload`).
2. **Open Swagger UI**: Navigate to `http://127.0.0` in your web browser.
3. **Authorize Sessions**: Click the **Authorize** button at the top right to input JWT tokens or user credentials for restricted role-based paths (e.g., Manager vs. Cashier roles).
4. **Execute Requests**: 
   * Expand any endpoint route (such as `POST /sales/` or `GET /products/{id}`).
   * Click **Try it out**.
   * Fill in the required parameters or JSON request body.
   * Click **Execute** to view real-time server responses, status codes (e.g., `200 OK`, `422 Unprocessable Entity`), and database transaction headers.
