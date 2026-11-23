# Sketchify - an E-Commerce site for Stationery & Art Supplies

> *"The vision is to create a space that reduces clutter and brings visual comfort in browsing to creative minds."*

**Sketchify** is a full-featured, aesthetic e-commerce web application designed for creative individuals, artists, and stationery lovers. It offers a warm, pastel-themed shopping experience with seamless category browsing, interactive cart management, dual payment gateways (Stripe & SSLCommerz), order invoice generation with email delivery, and a comprehensive admin management dashboard.

---

## Brand Design & Color Palette

Sketchify follows an intentional, warm pastel aesthetic:
- **Ambient Peach / Rose Tint:** `#fdeded` / `#fce2e8`
- **Sunset Wisteria / Purple:** `#c2aae3` (initial) / `#8f72b5` (hover)
- **Deep Teal Accent:** `#3c7a89` / `#2b5964`
- **Typography:** Comic Neue & clean sans-serif

---

## Project Architecture & Folder Structure

```text
Sketchify/
├── .env.example                  # Template for required environment variables
├── .gitignore                    # Git ignore file for secrets and environments
├── requirements.txt              # Python package dependencies
├── run.py                        # Application entry point (starts Flask app)
├── README.md                     # Comprehensive project documentation
│
└── app/                          # Core Flask Application Package
    ├── __init__.py               # App factory (create_app), extensions, blueprints
    │
    ├── controller/               # Business Logic & Database Controllers
    │   ├── admin_controller.py               # Admin auth, dashboard counts, CSV export
    │   ├── database_collection_controller.py # Centralized MongoDB collections accessor
    │   ├── order_controller.py               # Order creation & persistence logic
    │   └── user_controller.py                # User registration, login, backup codes, bcrypt
    │
    ├── routes/                   # Route Handlers & Blueprint Endpoints
    │   ├── admin_routes.py       # Admin login, dashboard, product & user management
    │   ├── cart_routes.py        # Add to cart (AJAX), view cart, update/remove items
    │   ├── category_routes.py    # Dynamic category product views (/categories/<name>)
    │   ├── checkout_routes.py    # Checkout redirect & login verification
    │   ├── default_routes.py     # Homepage, newsletter subscription, category redirects
    │   ├── order_routes.py       # User order history, print invoice, email invoice
    │   ├── payment_routes.py     # Stripe checkout session, success & cancel handlers
    │   ├── ssl_commerz_routes.py # SSLCommerz (bKash, Nagad, cards) integration
    │   └── user_routes.py        # User register, login, backup-code login, profile, search
    │
    ├── static/                   # Static Assets
    │   ├── Sketchify.png         # Main application logo
    │   ├── cart.svg              # Navigation cart icon
    │   ├── login.png             # Login / Register illustration mascot
    │   ├── css/                  # Modular Page Stylesheets
    │   │   ├── categories.css    # Category & product grid styling
    │   │   ├── homepage.css      # Homepage hero, category banner, featured items
    │   │   ├── login.css         # Mascot-framed login & backup-code auth page
    │   │   └── register.css      # User registration form with brand gradient
    │   └── images/
    │       └── MainPage/         # Homepage banners & category preview images
    │
    └── templates/                # Jinja2 HTML Templates
        ├── homepage.html         # Main landing page with hero banner & featured grid
        │
        └── Components/           # Modular Page Templates & Partial Views
            ├── navbar.html       # Persistent navigation header with live AJAX cart badge
            ├── footer.html       # Unified 4-column footer with newsletter & quick links
            ├── subnav.html       # Category filter chips navigation bar
            │
            ├── login.html             # User login page
            ├── login_with_backup.html # 8-digit backup code fallback authentication
            ├── register.html          # User registration form
            ├── userDashboard.html     # User profile overview
            ├── editUserProfile.html   # Update user credentials & information
            │
            ├── Admin/            # Admin Panel Views
            │   ├── admin_login.html   # Dedicated admin credentials login
            │   ├── dashboard.html     # Analytics (users, products, orders counts)
            │   ├── orders-list.html   # Order management, CSV export, delivery status
            │   ├── products-list.html # Inventory management (CRUD products)
            │   ├── sidebar.html       # Admin sidebar navigation
            │   └── users-list.html    # Registered customer accounts
            │
            ├── cart/
            │   └── cart.html          # Shopping cart overview & item quantity management
            │
            ├── categories/
            │   └── category.html      # Dynamic category product listing with AJAX cart
            │
            ├── Order/
            │   ├── user_order.html    # Customer order history table
            │   └── invoice.html       # Clean, printable A4 invoice
            │
            ├── Payment/
            │   └── payment_page.html  # Payment method selection (Stripe / SSLCommerz)
            │
            └── Search/
                └── search_results.html # Product search results page
```

---

## Tech Stack

- **Backend:** Python 3.10+, Flask, Jinja2, Gunicorn (Production)
- **Database:** MongoDB (Local or MongoDB Atlas) via `pymongo`
- **Authentication & Security:** Bcrypt password hashing, session-based auth, 8-digit emergency backup recovery codes
- **Payment Gateways:**
  - **Stripe:** International card payments (Checkout Sessions)
  - **SSLCommerz:** Bangladeshi local payments (bKash, Nagad, Rocket, local cards)
- **Email Service:** Flask-Mail (Gmail SMTP for sending backup codes & PDF-ready HTML invoices)
- **Frontend:** HTML5, CSS3, Bootstrap 5.3, JavaScript (AJAX Add-to-Cart with bounce animation & toast notifications)

---

## How to Run Locally (Local Setup Guide)

### 1. Prerequisites
Ensure you have the following installed on your machine:
- **Python 3.10+** (verify with `python --version`)
- **MongoDB** (Local MongoDB instance or a free MongoDB Atlas connection URI)
- **Git**

---

### 2. Clone the Repository
```bash
git clone https://github.com/anika-tabassum-tousi/Sketchify.git
cd Sketchify
```

---

### 3. Create and Activate Virtual Environment
On **Windows (Command Prompt / PowerShell)**:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

On **macOS / Linux**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 5. Configure Environment Variables (`.env`)
Create a `.env` file in the root project directory (or copy from `.env.example`):
```bash
cp .env.example .env
```

Open `.env` and fill in your configuration:
```ini
# MongoDB Connection (Local or Atlas)
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/

# Admin Dashboard Credentials
ADMIN_NAME=admin
ADMIN_PASS=admin123

# Flask Secret Key
SECRET_KEY=supersecretkey_sketchify_2026

# Flask-Mail (Optional: for sending invoices and backup codes via Gmail)
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password

# Payment Gateways (Optional: Test keys)
stripe_api_key=sk_test_...
SSLCOMMERZ_STORE_ID=your_store_id
SSLCOMMERZ_STORE_PASSWD=your_store_password
SSLCOMMERZ_IS_SANDBOX=true
```

---

### 6. Start the Application
Run the entry point script:
```bash
python run.py
```

The application will launch on:
**`http://127.0.0.1:5000/`** (or `http://localhost:5000/`)

---

## Key Application URLs

| Route | Description |
| :--- | :--- |
| `/` | Homepage with hero section, category shortcuts, and featured products |
| `/categories/new-in` | Category product listing (supports `art-supplies`, `stationaries`, `desk-organizers`, `gift-items`) |
| `/cart` | View shopping cart, modify quantities, and proceed to checkout |
| `/login` | User login |
| `/login-backup` | Emergency login using the 8-digit backup code |
| `/register` | User signup with automatic backup code generation |
| `/user-dashboard` | Customer dashboard & profile information |
| `/orders` | Customer order history, view invoice, email invoice |
| `/checkout` | Checkout verification & payment redirect |
| `/admin/login` | Dedicated Admin portal login |
| `/admin/dashboard` | Admin analytics, product management, orders, and CSV export |

---

## Admin Access
1. Navigate to `http://127.0.0.1:5000/admin/login`
2. Enter the credentials configured in your `.env`:
   - **Username:** `admin` (or your `ADMIN_NAME`)
   - **Password:** `admin123` (or your `ADMIN_PASS`)
3. Access real-time order tracking, CSV report downloads, and product catalog updates.

---

## Deployment (Render Cloud)
The repository includes configuration ready for Render:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn run:app`
- Set environment variables in the Render dashboard under **Environment**.
