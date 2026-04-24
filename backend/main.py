import os
import json
from fastapi import FastAPI, HTTPException, Header, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
import psycopg2.extras
import resend
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from datetime import datetime

load_dotenv()

app = FastAPI(title="Companion API", version="1.0.0")

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Cloudinary Config ────────────────────────────────────────────────────────
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME", "dpotignke"),
    api_key=os.environ.get("CLOUDINARY_API_KEY", "138683548794975"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET", "h45xcBAz-l2068nDE_SEOEuvxd0"),
    secure=True,
)

# ─── DB Helper ────────────────────────────────────────────────────────────────
def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"])


# ─── Models ───────────────────────────────────────────────────────────────────
class OrderItem(BaseModel):
    id: int
    name: str
    price: float
    quantity: int = 1

class Order(BaseModel):
    customer_name: str
    phone: str
    whatsapp: str
    address: str
    governorate: str
    payment_method: str  # "cash" or "vodafone_cash"
    items: List[OrderItem]
    notes: Optional[str] = ""

class Category(BaseModel):
    slug: str
    name: str
    description: Optional[str] = ""
    image_url: Optional[str] = ""

class Product(BaseModel):
    name: str
    category: str
    price: float
    description: str
    image_url: str       # Primary image (Cloudinary URL)
    images: List[str] = []  # Additional images (Cloudinary URLs)
    available: bool = True
    features: List[dict] = []
    discount_percentage: int = 0
    is_featured: bool = False
    is_package_featured: bool = False

class DiscountApply(BaseModel):
    target_type: str # 'category', 'product', or 'all'
    target_ids: List[str]   # List of slugs or product_ids as strings
    discount_percentage: int


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def read_root():
    return {"message": "Companion API is Running!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": str(datetime.now())}

# ─── Categories ───────────────────────────────────────────────────────────────
@app.get("/categories")
def get_categories():
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM categories ORDER BY id")
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()

@app.post("/admin/categories")
def add_category(category: Category, x_admin_token: str = Header(...)):
    admin_password = os.environ.get("ADMIN_PASSWORD", "Passw@rdcompanion$")
    if x_admin_token != admin_password:
        raise HTTPException(status_code=401, detail="Invalid admin token")
    
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO categories (slug, name, description, image_url)
               VALUES (%s, %s, %s, %s) ON CONFLICT (slug) DO UPDATE
               SET name = EXCLUDED.name, description = EXCLUDED.description, image_url = EXCLUDED.image_url RETURNING id""",
            (category.slug, category.name, category.description, category.image_url)
        )
        conn.commit()
        return {"status": "added"}
    finally:
        conn.close()


# ─── Discounts ────────────────────────────────────────────────────────────────
@app.put("/admin/discount/apply")
def apply_discount(payload: DiscountApply, x_admin_token: str = Header(...)):
    admin_password = os.environ.get("ADMIN_PASSWORD", "Passw@rdcompanion$")
    if x_admin_token != admin_password:
        raise HTTPException(status_code=401, detail="Invalid admin token")

    conn = get_db()
    try:
        cur = conn.cursor()
        if payload.target_type == "category":
            if not payload.target_ids:
                return {"status": "no change"}
            cur.execute("UPDATE products SET discount_percentage = %s WHERE category IN %s", (payload.discount_percentage, tuple(payload.target_ids)))
        elif payload.target_type == "product":
            if not payload.target_ids:
                return {"status": "no change"}
            ids = [int(x) for x in payload.target_ids]
            cur.execute("UPDATE products SET discount_percentage = %s WHERE id IN %s", (payload.discount_percentage, tuple(ids)))
        else:
            cur.execute("UPDATE products SET discount_percentage = %s", (payload.discount_percentage,))
        conn.commit()
        return {"status": "updated"}
    finally:
        conn.close()


# ─── Cloudinary Upload ────────────────────────────────────────────────────────
@app.post("/admin/upload")
async def upload_image(
    file: UploadFile = File(...),
    x_admin_token: str = Header(...)
):
    """Upload an image to Cloudinary and return its secure URL."""
    admin_password = os.environ.get("ADMIN_PASSWORD", "Passw@rdcompanion$")
    if x_admin_token != admin_password:
        raise HTTPException(status_code=401, detail="Invalid admin token")

    contents = await file.read()
    # Use the original filename (without extension) as the public_id
    filename = os.path.splitext(file.filename)[0].replace(" ", "_")

    result = cloudinary.uploader.upload(
        contents,
        folder="companion",
        public_id=filename,
        overwrite=True,
        resource_type="image",
    )
    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
    }


# ─── Products ─────────────────────────────────────────────────────────────────
@app.get("/products")
def get_products(category: Optional[str] = None):
    """Return all available products, optionally filtered by category."""
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if category:
            cur.execute(
                "SELECT * FROM products WHERE available = true AND category = %s ORDER BY id",
                (category,)
            )
        else:
            cur.execute("SELECT * FROM products WHERE available = true ORDER BY id")
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


@app.post("/admin/product")
def add_product(product: Product, x_admin_token: str = Header(...)):
    """Add a new product to the database."""
    admin_password = os.environ.get("ADMIN_PASSWORD", "Passw@rdcompanion$")
    if x_admin_token != admin_password:
        raise HTTPException(status_code=401, detail="Invalid admin token")

    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO products (name, category, price, description, image_url, images, available, features, discount_percentage, is_featured, is_package_featured)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
            (product.name, product.category, product.price,
             product.description, product.image_url,
             json.dumps(product.images),
             product.available, json.dumps(product.features), product.discount_percentage,
             product.is_featured, product.is_package_featured)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return {"status": "added", "id": new_id}
    finally:
        conn.close()


@app.put("/admin/product/{product_id}")
def update_product(product_id: int, product: Product, x_admin_token: str = Header(...)):
    """Update an existing product."""
    admin_password = os.environ.get("ADMIN_PASSWORD", "Passw@rdcompanion$")
    if x_admin_token != admin_password:
        raise HTTPException(status_code=401, detail="Invalid admin token")

    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(
            """UPDATE products
               SET name = %s, category = %s, price = %s, description = %s,
                   image_url = %s, images = %s, available = %s, features = %s, 
                   discount_percentage = %s, is_featured = %s, is_package_featured = %s
               WHERE id = %s RETURNING id""",
            (product.name, product.category, product.price,
             product.description, product.image_url,
             json.dumps(product.images),
             product.available, json.dumps(product.features), product.discount_percentage, 
             product.is_featured, product.is_package_featured, product_id)
        )
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Product not found")
        conn.commit()
        return {"status": "updated", "id": product_id}
    finally:
        conn.close()


@app.delete("/admin/product/{product_id}")
def delete_product(product_id: int, x_admin_token: str = Header(...)):
    """Soft-delete (mark unavailable) a product."""
    admin_password = os.environ.get("ADMIN_PASSWORD", "Passw@rdcompanion$")
    if x_admin_token != admin_password:
        raise HTTPException(status_code=401, detail="Invalid admin token")

    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE products SET available = false WHERE id = %s", (product_id,))
        conn.commit()
        return {"status": "removed"}
    finally:
        conn.close()


@app.post("/order")
def place_order(order: Order):
    """Receive an order and email it to the store owner via Resend."""
    resend.api_key = os.environ["RESEND_API_KEY"]
    owner_email = os.environ["OWNER_EMAIL"]

    items_text = "\n".join(
        [f"  • {item.name}  x{item.quantity}  —  {item.price * item.quantity:.2f} EGP"
         for item in order.items]
    )
    total = sum(item.price * item.quantity for item in order.items)
    payment_label = "Vodafone Cash 📱" if order.payment_method == "vodafone_cash" else "Cash on Delivery 💵"

    html_body = f"""
    <h2 style="color:#6C63FF;">🛍️ New Companion Order!</h2>
    <table style="font-family:sans-serif;font-size:15px;border-collapse:collapse;width:100%">
      <tr><td><b>Customer</b></td><td>{order.customer_name}</td></tr>
      <tr><td><b>Phone</b></td><td>{order.phone}</td></tr>
      <tr><td><b>WhatsApp</b></td><td>{order.whatsapp}</td></tr>
      <tr><td><b>Address</b></td><td>{order.address}, {order.governorate}</td></tr>
      <tr><td><b>Payment</b></td><td>{payment_label}</td></tr>
      <tr><td><b>Notes</b></td><td>{order.notes or "—"}</td></tr>
    </table>
    <h3 style="margin-top:20px;">📦 Items</h3>
    <pre style="background:#f5f5f5;padding:12px;border-radius:8px">{items_text}</pre>
    <h3>💰 Total: {total:.2f} EGP</h3>
    <p style="color:#888;font-size:12px;">Contact the customer on WhatsApp to confirm & arrange delivery.</p>
    """

    resend.Emails.send({
        "from": "Companion Orders <onboarding@resend.dev>",
        "to": owner_email,
        "subject": f"🛍️ New Order from {order.customer_name} — {total:.2f} EGP",
        "html": html_body,
    })

    return {"status": "success", "message": "Order received! We'll contact you on WhatsApp soon."}
