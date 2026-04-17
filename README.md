# DivineCo - Cookie Ordering & Business Management System

<p align="center">
  <img src="https://customer-assets.emergentagent.com/job_divine-orders/artifacts/evhnjrbq_logo.png.png" alt="Divine Co. Logo" width="200"/>
</p>

## Overview

**DivineCo** is a modern web-based system for a cookie business that functions as both a **Customer Ordering Website** and an **Admin Dashboard** with inventory tracking. Customers can browse cookie flavors, add items to cart, and place orders with GCash payment. Administrators can view all orders, track inventory per flavor in real-time, and monitor sales summaries.

**Live URL:** [DivineCoshop.com](https://divine-orders.preview.emergentagent.com)

---

## Features

### Customer Side
- Browse 6 premium cookie flavors with images
- Two pricing options per flavor: Per Piece (₱45) and Box of 6 (₱260)
- Add to cart with quantity adjustment (+/-)
- Live total price calculation in Philippine Peso (₱)
- Checkout with customer info (Name, Phone, Address)
- Order confirmation receipt with GCash payment details
- Mobile-responsive design

### Admin Dashboard
- Protected login (username & password authentication)
- Order management table (Name, Phone, Address, Items, Total, Payment, Status, Date)
- Real-time inventory tracking per flavor (pieces sold, boxes sold, total)
- Sales summary: total orders, total revenue, best-selling flavor
- Mark orders as completed
- Logout functionality

---

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| **Frontend** | React 19, Tailwind CSS, Shadcn/UI   |
| **Backend**  | Python (FastAPI), Uvicorn           |
| **Database** | MongoDB (Motor async driver)        |
| **Routing**  | React Router DOM v7                 |
| **HTTP**     | Axios                               |
| **Icons**    | Lucide React                        |
| **Toasts**   | Sonner                              |

---

## Project Structure

```
project-root/
├── backend/
│   ├── server.py              # FastAPI application (models, routes, logic)
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables (MONGO_URL, DB_NAME)
├── frontend/
│   ├── public/
│   │   └── index.html         # HTML entry point
│   ├── src/
│   │   ├── index.js           # React entry point
│   │   ├── index.css          # Global styles + Tailwind + CSS variables
│   │   ├── App.js             # Router setup
│   │   ├── App.css            # Custom animations & table styles
│   │   ├── components/
│   │   │   ├── CustomerStorefront.js  # Main storefront page
│   │   │   ├── ProductCard.js         # Individual cookie card
│   │   │   ├── CartSheet.js           # Slide-out cart drawer
│   │   │   ├── CheckoutModal.js       # Checkout form modal
│   │   │   ├── OrderConfirmation.js   # Receipt after order
│   │   │   ├── AdminLogin.js          # Admin login page
│   │   │   ├── AdminDashboard.js      # Admin main dashboard
│   │   │   ├── SalesSummaryCards.js   # Stats cards component
│   │   │   ├── InventoryTracking.js   # Inventory grid component
│   │   │   ├── OrdersTable.js         # Orders table component
│   │   │   └── ui/                    # Shadcn UI components
│   │   ├── hooks/
│   │   │   ├── useCart.js             # Cart state management hook
│   │   │   └── use-toast.js           # Toast hook
│   │   └── lib/
│   │       └── utils.js               # Utility functions
│   ├── package.json           # Node.js dependencies
│   └── .env                   # Frontend env (REACT_APP_BACKEND_URL)
├── memory/
│   ├── PRD.md                 # Product Requirements Document
│   └── test_credentials.md    # Admin credentials for testing
└── README.md                  # This file
```

---

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- MongoDB

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/divineco.git
   cd divineco
   ```

2. **Backend setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend setup:**
   ```bash
   cd frontend
   yarn install
   ```

4. **Environment variables:**

   Backend `.env`:
   ```
   MONGO_URL="mongodb://localhost:27017"
   DB_NAME="test_database"
   CORS_ORIGINS="*"
   ```

   Frontend `.env`:
   ```
   REACT_APP_BACKEND_URL=http://localhost:8001
   ```

5. **Run the application:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload

   # Terminal 2 - Frontend
   cd frontend
   yarn start
   ```

6. **Access the app:**
   - Customer Storefront: `http://localhost:3000`
   - Admin Login: `http://localhost:3000/admin/login`

---

## API Endpoints

| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| GET    | `/api/`               | Health check               |
| POST   | `/api/orders`         | Create a new order         |
| GET    | `/api/orders`         | Get all orders             |
| PATCH  | `/api/orders/{id}`    | Update order status        |
| GET    | `/api/inventory`      | Get inventory & sales data |
| POST   | `/api/admin/login`    | Admin authentication       |

---

## Cookie Flavors

| Flavor          | Per Piece | Box of 6 |
|-----------------|-----------|----------|
| Chocolate Chips | ₱45       | ₱260     |
| White Matcha    | ₱45       | ₱260     |
| Deep Choco      | ₱45       | ₱260     |
| S'mores         | ₱45       | ₱260     |
| Monster Cookie  | ₱45       | ₱260     |
| Cheesy Velvet   | ₱45       | ₱260     |

---

## Contributors

- **Dragon, Diven Mark C.** — TCPE 2-1

---

## License

This project is developed for academic and business purposes for DivineCo.
