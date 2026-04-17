# DivineCo PRD

## Original Problem Statement
Build a modern web-based system for a cookie business called "DivineCo" — a customer ordering website + admin dashboard with inventory tracking.

## Architecture
- **Backend**: FastAPI + MongoDB (Motor async driver)
- **Frontend**: React + Tailwind CSS + Shadcn UI
- **Auth**: Simple username/password for admin (stored server-side)
- **Database**: MongoDB (orders collection)

## User Personas
1. **Customer**: Orders cookies via storefront, pays via GCash
2. **Admin**: Manages orders, tracks inventory, views sales summary

## Core Requirements (Static)
- 6 cookie flavors with per-piece (₱45) and box-of-6 (₱260) pricing
- Cart with quantity adjustment and live total
- GCash payment display (09614841216)
- Admin dashboard: orders table, inventory tracking, sales summary
- Admin route protection with login

## What's Been Implemented
- [Feb 2026] Full customer storefront with product catalog, cart, checkout
- [Feb 2026] Admin login (Admin/vxnz.exe) with route protection
- [Feb 2026] Admin dashboard: orders management, inventory tracking, sales summary
- [Feb 2026] Order status management (pending → completed)
- [Apr 2026] Code quality refactor: extracted smaller components (ProductCard, CartSheet, CheckoutModal, OrdersTable, SalesSummaryCards, InventoryTracking, useCart hook)
- [Apr 2026] Fixed hook dependencies, array index keys, removed console statements
- [Apr 2026] Custom cookie images uploaded (all 6 flavors)
- [Apr 2026] Divine Co. logo integrated across nav, login, admin
- [Apr 2026] Page title set to DivineCoshop.com
- [Apr 2026] Admin link added to storefront nav
- [Apr 2026] Order confirmation receipt with GCash payment info
- [Apr 2026] Fixed cart Sheet overlay blocking checkout modal
- [Apr 2026] Toast position moved to bottom-center

## Prioritized Backlog
- P1: CSV/Excel export for orders
- P1: Order deletion for admin
- P2: SMS notifications on order status change
- P2: Order search/filter in admin
- P3: Customer order tracking page
- P3: Save receipt as image button
