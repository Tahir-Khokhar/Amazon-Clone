# 🛒 Amazon Clone - Full-Stack E-Commerce Platform

> A feature-rich eCommerce platform built with **Django 6** and **Django REST Framework**, inspired by Amazon's core functionality. This project delivers a complete online marketplace experience with a robust REST API, JWT authentication, Celery async tasks, Swagger documentation, and a Django template-based frontend. Includes advanced AI-powered recommendations, customer-seller chat, bulk data import/export, product comparison, Q&A system, referral rewards, checkout sessions, newsletter subscriptions, and comprehensive return management.

---

## ✨ Features

### 🔐 Authentication & Authorization
- JWT-based authentication (access + refresh tokens)
- Role-based access control: `Admin`, `Seller`, `Customer`, `Delivery Staff`
- User registration, login, profile management
- Email verification support
- Token blacklisting on logout

### 📦 Product Management
- Full CRUD with categories, brands, and tags
- Product variants (size, color, SKU) with own pricing & stock
- Multiple product images with primary image support
- Product specifications (key-value pairs)
- Attributes & attribute values
- Inventory tracking with low-stock alerts
- Auto-slug generation
- Featured products, discount pricing, barcode support

### 🛒 Shopping Cart & Wishlist
- Session-based cart for guests, user-based cart for logged-in users
- Save items for later
- Cart merging on login
- Product wishlist with variant support

### 📋 Order Management
- Full order lifecycle: `Pending → Confirmed → Packed → Shipped → Out for Delivery → Delivered`
- Order cancellation, returns, and refunds
- Order items with product snapshots
- Unique order number generation
- Coupon integration with discount calculations

### 💳 Payments
- Multiple payment gateways: **COD, Stripe, PayPal, JazzCash, EasyPaisa, Bank Transfer**
- Payment transaction tracking with JSON metadata
- Refund support

### 🚚 Shipping
- Multiple shipping methods with cost estimation
- Shipping address management
- Shipment tracking with courier names & tracking numbers
- Delivery date estimation

### 🏷️ Coupons & Discounts
- Flat, percentage, and free-shipping coupon types
- Usage limits, minimum purchase, and max discount caps
- Coupon usage tracking per user

### ⭐ Reviews & Ratings
- Star ratings (1–5) with text reviews
- Review images
- Verified purchase badges
- Helpful votes / like system
- Admin approval workflow

### 🔍 Search
- Full-text search across product names & descriptions
- Search query logging for analytics
- Popular search trends tracking
- Search history per user

### 📊 Admin Dashboard & Analytics
- Real-time dashboard stats (orders, revenue, users, products)
- Page view analytics with referrer tracking
- Product view tracking
- Sales reports with top products & categories
- Revenue reporting

### 👥 Seller Management
- Seller profiles with store branding (logo, banner)
- Commission rate tracking
- Sales & revenue tracking per seller
- Seller verification workflow

### 👤 Customer Profiles
- Loyalty points system
- Premium customer tiers
- Order history & spending tracking

### 🔔 Notifications
- Real-time notifications for orders, offers, wishlist alerts, support updates
- Read/unread tracking with JSON metadata

### 🆘 Support System
- FAQ management with categories
- Support tickets with priority levels (low → urgent)
- Ticket messaging with file attachments
- Ticket lifecycle: Open → In Progress → Resolved → Closed

### 🏠 Frontend (Django Templates)
- Home page with featured products
- Product listing with search & category filtering
- Product detail with related products
- Categories page with product counts
- Deals page (discounted products)
- Cart page with address selection
- Wishlist, Profile, Order History pages
- Support, FAQ, Contact Us pages

### 🧠 AI Recommendations
- Product-to-product recommendations with scores & reasons
- User preference tracking by category
- Personalized suggestions per user history
- Collaborative filtering-style recommendations

### 💬 Customer-Seller Chat
- Dedicated chat rooms between customers and sellers
- Real-time message history
- Read/unread message tracking
- Chat room listing and management

### 🔁 Product Q&A
- Product-specific questions and answers
- Official answers from sellers
- Helpful vote counts on answers
- Q&A listings per product

### ⚖️ Product Compare
- Compare up to 4 products side-by-side
- Persistent compare lists per user
- Add/remove/clear comparison items

### 📜 Browsing History
- Track recently viewed products per user
- Clear browsing history option
- Ordered by most-recently viewed

### 🎁 Referrals & Rewards
- Unique referral codes per user
- Referral reward tracking upon completed orders
- Referral status lifecycle (Pending → Completed → Cancelled)

### 🛎️ Checkout Session
- Multi-step checkout sessions (products, shipping, tax, totals)
- Checkout persistence across page reloads
- Automatic subtotal/tax/shipping/grand-total calculation

### 📦 Bulk Operations
- Bulk product import via CSV/Excel
- Bulk category/brand import
- Import job status tracking (pending/processing/completed/failed)
- Product export functionality

### 🔄 Returns & Replacements
- Dedicated return request system (return/replacement/refund)
- Return reason categorization (defective, wrong item, not as described, etc.)
- Return status workflow (Pending → Approved → Rejected → Processing → Completed → Cancelled)
- Admin notes, refund amounts, and image uploads

### 📰 Newsletter & Subscriptions
- Newsletter/email subscription support
- Premium subscription plans (monthly/yearly)
- Subscription lifecycle management (pending/active/cancelled/expired)

### 📄 Policy Pages
- Shipping policy, return policy, privacy policy, terms & conditions
- Admin-manageable via Site Configuration

### ⚙️ Site Configuration
- Admin-controlled site settings (site name, currency, tax rate, shipping costs)
- Return window days, auto-approve returns, refund processing days
- Support hours, SLA response times, contact information

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Django 6.0.7** | Web framework |
| **Django REST Framework 3.17.1** | REST API |
| **SimpleJWT** | JWT authentication |
| **Celery 5.6.3** | Async task queue |
| **Redis** | Message broker & caching |
| **SQLite** (dev) / PostgreSQL (prod) | Database |
| **drf-spectacular** | OpenAPI/Swagger documentation |
| **django-filter** | Advanced filtering |
| **django-cors-headers** | CORS support |
| **django-jazzmin** | Modern admin panel UI |
| **Whitenoise** | Static file serving |
| **Pillow** | Image processing |
| **Gunicorn** | Production WSGI server |

---

## 📁 Project Structure

```
Amazon_Clone/
├── config/                      # Django project configuration
│   ├── config/
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # Root URL configuration
│   │   ├── celery.py           # Celery configuration
│   │   ├── wsgi.py / asgi.py   # WSGI/ASGI entry points
│   │   └── __init__.py
│   ├── apps/                    # All Django apps
│   │   ├── accounts/           # User auth & profiles
│   │   ├── addresses/          # Shipping & billing addresses
│   │   ├── analytics/          # Page & product view tracking
│   │   ├── brands/             # Product brand management
│   │   ├── browsing_history/   # User browsing history tracking
│   │   ├── bulk_operations/    # Bulk import/export operations
│   │   ├── cart/               # Shopping cart
│   │   ├── categories/         # Product categories
│   │   ├── chat/               # Customer-seller chat rooms
│   │   ├── checkout/           # Checkout sessions
│   │   ├── core/               # Abstract base models & site config
│   │   ├── coupons/            # Discount coupons
│   │   ├── customers/          # Customer profiles
│   │   ├── dashboard/          # Admin dashboard stats
│   │   ├── frontend/           # Django template views (home, products, etc.)
│   │   ├── notifications/      # User notifications
│   │   ├── orders/             # Order management
│   │   ├── payments/           # Payment processing
│   │   ├── product_compare/    # Product comparison lists
│   │   ├── product_qa/         # Product Q&A system
│   │   ├── products/           # Product CRUD, variants, images
│   │   ├── recommendations/    # AI product recommendations
│   │   ├── referrals/          # Referral codes & rewards
│   │   ├── reports/            # Sales & analytics reports
│   │   ├── returns/            # Return & replacement management
│   │   ├── reviews/            # Product reviews & ratings
│   │   ├── search/             # Search functionality
│   │   ├── sellers/            # Seller profiles
│   │   ├── shipping/           # Shipping methods & tracking
│   │   ├── support/            # FAQs & support tickets
│   │   └── wishlist/           # User wishlists
│   ├── static/                  # Static assets (CSS, JS)
│   ├── templates/               # Django HTML templates
│   │   └── frontend/           # Frontend page templates
│   ├── manage.py                # Django management script
│   └── requirements.txt        # Python dependencies
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Redis (for Celery & caching)
- pip / pipenv

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/amazon-clone.git
cd amazon-clone/config

# 2. Create a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Create a superuser
python manage.py createsuperuser

# 6. Load sample data (optional)
python manage.py loaddata fixtures/users.json
python populate_products.py
python generate_all_product_images.py

# 7. Run the development server
python manage.py runserver
```

### Start Celery (for async tasks)

```bash
# Start Redis (if not running)
redis-server

# Start Celery worker
celery -A config worker -l info

# Start Celery beat (for scheduled tasks)
celery -A config beat -l info
```

---

## 📖 API Reference

The API is fully documented with **Swagger** and **ReDoc**.

| Documentation | URL |
|---------------|-----|
| Swagger UI | `http://localhost:8000/api/docs/` |
| ReDoc | `http://localhost:8000/api/redoc/` |
| OpenAPI Schema | `http://localhost:8000/api/schema/` |

### API Endpoints Overview

| Endpoint | Description |
|----------|-------------|
| `POST /api/auth/register/` | User registration |
| `POST /api/auth/login/` | JWT login (access + refresh tokens) |
| `POST /api/auth/token/refresh/` | Refresh access token |
| `POST /api/auth/logout/` | Logout (blacklist token) |
| `GET /api/auth/profile/` | View/update user profile |
| `GET /api/products/` | List products (paginated) |
| `GET /api/products/{slug}/` | Product detail |
| `POST /api/products/` | Create product (seller/admin) |
| `GET /api/categories/` | List categories |
| `GET /api/brands/` | List brands |
| `GET /api/cart/` | Get current cart |
| `POST /api/cart/add/` | Add item to cart |
| `GET /api/wishlist/` | Get wishlist |
| `POST /api/orders/` | Create order |
| `GET /api/orders/` | List user orders |
| `POST /api/payments/` | Process payment |
| `GET /api/coupons/` | List active coupons |
| `POST /api/coupons/apply/` | Apply coupon to cart |
| `GET /api/reviews/?product={id}` | List product reviews |
| `POST /api/reviews/` | Create review |
| `GET /api/notifications/` | List user notifications |
| `GET /api/search/?q={query}` | Search products |
| `GET /api/shipping/methods/` | List shipping methods |
| `POST /api/support/tickets/` | Create support ticket |
| `GET /api/dashboard/stats/` | Dashboard statistics (admin) |
| `GET /api/reports/sales/` | Sales reports (admin) |
| `GET /api/analytics/page-views/` | Page view analytics (admin) |
| `GET /api/browsing-history/` | User browsing history |
| `POST /api/browsing-history/clear/` | Clear browsing history |
| `GET /api/product-compare/` | View compare list |
| `POST /api/product-compare/add/<id>/` | Add product to compare |
| `POST /api/product-compare/remove/<id>/` | Remove product from compare |
| `POST /api/product-compare/clear/` | Clear compare list |
| `GET /api/product-qa/products/<slug>/questions/` | Product Q&A |
| `POST /api/product-qa/products/<slug>/questions/` | Ask a question |
| `POST /api/product-qa/questions/<id>/answers/` | Answer a question |
| `GET /api/chat/rooms/` | List chat rooms |
| `POST /api/chat/rooms/create/` | Create chat room with seller |
| `GET /api/chat/rooms/<id>/messages/` | Get chat messages |
| `POST /api/chat/rooms/<id>/messages/` | Send message |
| `GET /api/recommendations/my/` | Personalized recommendations |
| `GET /api/recommendations/products/<slug>/` | Related product recommendations |
| `POST /api/recommendations/generate/` | Generate recommendations |
| `POST /api/checkout/create/` | Create checkout session |
| `POST /api/checkout/confirm/` | Confirm & place order |
| `GET /api/returns/` | List return requests |
| `POST /api/returns/create/` | Create return request |
| `POST /api/returns/<id>/admin-update/` | Admin update return |
| `GET /api/referrals/my-code/` | Get my referral code |
| `GET /api/referrals/list/` | List referral history |
| `POST /api/referrals/apply/` | Apply referral code |
| `POST /api/bulk/import/` | Import products/categories/brands |
| `GET /api/bulk/imports/` | List import jobs |
| `GET /api/bulk/export/products/` | Export products |

> **Note:** Most endpoints require authentication via `Authorization: Bearer <token>` header. Role-based permissions apply to seller/admin endpoints.

---

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test apps.products
python manage.py test apps.orders
python manage.py test apps.payments
```

---

## 📦 Key Django Apps & Responsibilities

| App | Responsibility |
|-----|---------------|
| `accounts` | User model, JWT auth, profiles, role management |
| `products` | Product CRUD, variants, images, attributes, inventory |
| `categories` | Hierarchical categories (parent/child) |
| `brands` | Brand management with logos |
| `cart` | Session & user-based shopping cart |
| `wishlist` | User wishlist management |
| `orders` | Full order lifecycle with items |
| `payments` | Multi-gateway payment processing |
| `shipping` | Shipping methods, addresses, tracking |
| `coupons` | Discount coupon system |
| `reviews` | Product reviews, ratings, likes |
| `notifications` | User notification system |
| `addresses` | Shipping & billing address management |
| `search` | Search tracking & popular searches |
| `dashboard` | Admin dashboard statistics |
| `reports` | Sales reports, top products & categories |
| `analytics` | Page & product view tracking |
| `support` | FAQ management & support tickets |
| `sellers` | Seller profiles, store management, commissions |
| `customers` | Customer profiles, loyalty points |
| `frontend` | Django template-based frontend views |
| `browsing_history` | User browsing history tracking |
| `bulk_operations` | Bulk product/category/brand import & export |
| `chat` | Customer-seller chat rooms & messaging |
| `checkout` | Multi-step checkout sessions |
| `product_compare` | Side-by-side product comparison |
| `product_qa` | Product Q&A with official answers |
| `recommendations` | AI-powered product recommendations & user preferences |
| `referrals` | Referral codes, tracking & rewards |
| `returns` | Return, replacement & refund requests |
| `core` | Base models, site configuration, newsletter & subscriptions |

---

## 🔧 Environment Variables

Create a `.env` file in the `config/` directory:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
FRONTEND_URL=http://localhost:3000
DEFAULT_FROM_EMAIL=noreply@amazonclone.com
```

---

## 🌐 Frontend Pages

The project includes a Django template-based frontend served at `http://localhost:8000/`:

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Featured products showcase |
| Products | `/products/` | Product listing with search & filters |
| Product Detail | `/products/{slug}/` | Full product view with images & specs |
| Categories | `/categories/` | All categories with product counts |
| Deals | `/deals/` | Discounted products |
| Cart | `/cart/` | Shopping cart with address selection |
| Wishlist | `/wishlist/` | Saved items |
| Login | `/login/` | User login |
| Register | `/register/` | User registration |
| Profile | `/profile/` | User account settings |
| Orders | `/orders/` | Order history |
| Support | `/support/` | Support ticket creation |
| FAQs | `/faqs/` | Frequently asked questions |
| Contact Us | `/contact/` | Contact form |
| Create Return | `/returns/create/` | Request a return or replacement |
| Shipping Policy | `/shipping-policy/` | Shipping information |
| Return Policy | `/return-policy/` | Return & exchange policy |
| Privacy Policy | `/privacy-policy/` | Privacy policy |
| Terms | `/terms/` | Terms & conditions |
| Premium Sub | `/subscribe/premium/` | Premium subscription plans |

---

## 🗺️ Roadmap

- [x] User authentication & role management
- [x] Product CRUD with variants & images
- [x] Shopping cart & wishlist
- [x] Order management with full lifecycle
- [x] Multi-gateway payment processing
- [x] Shipping & tracking
- [x] Coupon & discount system
- [x] Reviews & ratings
- [x] Admin dashboard & analytics
- [x] Search functionality
- [x] Browsing history tracking
- [x] Product compare & Q&A
- [x] Customer-seller chat
- [x] AI-powered recommendations
- [x] Referral rewards system
- [x] Checkout sessions
- [x] Bulk import/export
- [x] Returns & replacements management
- [x] Newsletter & premium subscriptions
- [x] Policy pages & site configuration
- [ ] Push notifications (WebSocket)
- [ ] Mobile app API optimization
- [ ] Multi-language support
- [ ] Multi-currency support
- [ ] Advanced recommendation engine (ML-based)
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code
- Use descriptive variable and function names
- Write docstrings for all public methods
- Add type hints where applicable

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by [Amazon.com](https://amazon.com)
- Built with [Django](https://www.djangoproject.com/) & [Django REST Framework](https://www.django-rest-framework.org/)
- Admin UI powered by [django-jazzmin](https://django-jazzmin.readthedocs.io/)
- API documentation via [drf-spectacular](https://drf-spectacular.readthedocs.io/)

---

## 📬 Contact

For questions, suggestions, or support, please open an issue on GitHub or contact the maintainer.

---

<p align="center">Made with ❤️ using Django & Django REST Framework</p>

