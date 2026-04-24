# Companion — E-Commerce Website 🩺
> *A Nurse From The Future*

A full-stack e-commerce site for medical accessories. Static frontend on **GitHub Pages**, minimal FastAPI backend on **Render**, database on **Neon**, emails via **Resend**.

---

## Project Structure
```
Companion/
├── backend/
│   ├── main.py           # FastAPI app (3 routes)
│   ├── requirements.txt  # Python dependencies
│   ├── Procfile          # Render start command
│   └── .env.example      # Environment variables template
├── database/
│   └── schema.sql        # Run once on Neon
├── frontend/
│   ├── index.html        # Home page
│   ├── shop.html         # Product catalog
│   ├── checkout.html     # Cart & order form
│   ├── admin.html        # Hidden admin panel
│   ├── style.css         # Shared design system
│   └── cart.js           # Shared cart logic
└── render.yaml           # Render deployment config
```

---

## Step-by-Step Setup

### Step 1 — Neon Database
1. Create a free account at [neon.tech](https://neon.tech)
2. Create a new project → copy the connection string
3. Open the SQL editor and paste the contents of `database/schema.sql`
4. Run it → table is created and 12 sample products are inserted

### Step 2 — Resend Email
1. Create a free account at [resend.com](https://resend.com)
2. Add & verify your domain (or use the default `onboarding@resend.dev` sandbox for testing)
3. Create an API key → copy it

### Step 3 — Deploy Backend to Render
1. Push your code to a GitHub repo
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repo → Render detects `render.yaml` automatically
4. In **Environment Variables**, add:
   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | Your Neon connection string |
   | `RESEND_API_KEY` | Your Resend API key |
   | `OWNER_EMAIL` | Your email address |
   | `ADMIN_PASSWORD` | A strong password (match what's in `admin.html`) |
5. Click **Deploy** → wait ~2 minutes
6. Copy your Render URL: `https://companion-api.onrender.com`

### Step 4 — Update Frontend API URL
In **both** `shop.html` and `checkout.html` and `admin.html`, find:
```js
const API_BASE = 'https://YOUR-RENDER-APP.onrender.com';
```
Replace with your actual Render URL.

Also in `admin.html`, update the password to match your `ADMIN_PASSWORD`:
```js
const CORRECT_PASSWORD = 'companion2024'; // ← change this
```

### Step 5 — Deploy Frontend to GitHub Pages
1. Push the contents of the `frontend/` folder to a GitHub repo
2. Go to **Settings → Pages** → Source: `main` branch, `/ (root)` folder
3. Wait ~60 seconds → your site is live at `https://username.github.io/repo-name`

### Step 6 — Prevent Render Spin-Down (Free Tier)
On the free Render tier, the API sleeps after 15 minutes of inactivity.

1. Go to [cron-job.org](https://cron-job.org) → Create a free account
2. New cronjob → URL: `https://companion-api.onrender.com/products`
3. Schedule: every **14 minutes**
4. Save → Done. Your API stays awake 24/7.

### Step 7 — Upload Products (Admin Panel)
1. Upload your catalog images to [Cloudinary](https://cloudinary.com) → copy the URLs
2. Open your site at `/admin.html`
3. Enter your admin password
4. Fill in the form and paste Cloudinary URLs → products appear live in the shop instantly

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/products` | All available products (optional `?category=id_holder`) |
| `POST` | `/order` | Place an order → sends email to owner |
| `POST` | `/admin/product` | Add product (requires `X-Admin-Token` header) |
| `DELETE` | `/admin/product/{id}` | Soft-delete product (requires `X-Admin-Token`) |

---

## Product Categories
| Key | Label |
|-----|-------|
| `id_holder` | 🪪 ID Holder |
| `note` | 📓 Nursing Note |
| `card` | 🃏 Medical Card |
| `pen_holder` | 🖊️ Pen Holder |

---

## Environment Variables Reference
```env
DATABASE_URL=postgresql://user:password@host/db?sslmode=require
RESEND_API_KEY=re_xxxxxxxxxxxxxx
OWNER_EMAIL=your@email.com
ADMIN_PASSWORD=your_strong_password
```
