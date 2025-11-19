# Database Quick Start Guide

## What Was Created

### Complete Database Schema
13 tables for a full-featured artist merch e-commerce platform:

1. **users** - Customer authentication and profiles
2. **artists** - Local artists with profiles and commission tracking
3. **categories** - Product categorization with hierarchy support
4. **products** - Main product information
5. **product_variants** - Sizes, colors, styles with individual pricing/inventory
6. **product_images** - Multiple images per product
7. **addresses** - Shipping and billing addresses
8. **cart_items** - Persistent shopping cart
9. **orders** - Purchase orders
10. **order_items** - Items within orders (with snapshots)
11. **payments** - Payment transaction records
12. **reviews** - Product reviews and ratings
13. **inventory_logs** - Track stock changes (audit trail)

See `DATABASE_SCHEMA.md` for complete schema documentation.

## Files Created

### Models (SQLAlchemy)
- `app/models/user.py` - User model
- `app/models/artist.py` - Artist model
- `app/models/category.py` - Category model
- `app/models/product.py` - Product, ProductVariant, ProductImage
- `app/models/address.py` - Address model
- `app/models/cart.py` - CartItem model
- `app/models/order.py` - Order, OrderItem models
- `app/models/payment.py` - Payment model
- `app/models/review.py` - Review model
- `app/models/inventory.py` - InventoryLog model

### Schemas (Pydantic)
- `app/schemas/user.py` - User validation schemas
- `app/schemas/artist.py` - Artist validation schemas
- `app/schemas/product.py` - Product, variant, image schemas
- `app/schemas/cart.py` - Cart validation schemas
- `app/schemas/order.py` - Order validation schemas

### API Routes
- `app/routes/products.py` - Product CRUD endpoints
- `app/routes/artists.py` - Artist CRUD endpoints

### Database
- `alembic/` - Database migration system configured
- `y2k_shopping.db` - SQLite database created
- All tables created and ready to use

## Testing the API

### Start the Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# OR use the startup script
./start-backend.sh
```

### Access API Documentation
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### Available Endpoints

**Artists:**
- `GET /api/v1/artists` - List all artists
- `GET /api/v1/artists/{id}` - Get artist by ID
- `GET /api/v1/artists/slug/{slug}` - Get artist by slug
- `POST /api/v1/artists` - Create artist
- `PATCH /api/v1/artists/{id}` - Update artist
- `DELETE /api/v1/artists/{id}` - Deactivate artist

**Products:**
- `GET /api/v1/products` - List all products (with filters)
- `GET /api/v1/products/{id}` - Get product with variants and images
- `GET /api/v1/products/slug/{slug}` - Get product by slug
- `POST /api/v1/products` - Create product
- `PATCH /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Deactivate product

## Testing with Sample Data

### 1. Create an Artist
```bash
curl -X POST http://localhost:8000/api/v1/artists \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Chen",
    "slug": "sarah-chen",
    "bio": "Y2K inspired digital artist specializing in retro-futuristic designs",
    "commission_rate": 15.00,
    "is_active": true,
    "featured": true
  }'
```

### 2. Create a Product
```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "artist_id": 1,
    "name": "Cyber Sunset T-Shirt",
    "slug": "cyber-sunset-tshirt",
    "description": "100% cotton tee with vibrant Y2K sunset gradient print",
    "short_description": "Y2K sunset gradient tee",
    "product_type": "physical",
    "base_price": 29.99,
    "is_active": true,
    "featured": true,
    "variants": [
      {
        "sku": "CYBER-SUNSET-S-BLACK",
        "name": "Small - Black",
        "size": "S",
        "color": "Black",
        "price": 29.99,
        "stock_quantity": 50,
        "requires_shipping": true,
        "is_active": true
      },
      {
        "sku": "CYBER-SUNSET-M-BLACK",
        "name": "Medium - Black",
        "size": "M",
        "color": "Black",
        "price": 29.99,
        "stock_quantity": 75,
        "requires_shipping": true,
        "is_active": true
      }
    ],
    "images": [
      {
        "image_url": "https://example.com/cyber-sunset-front.jpg",
        "alt_text": "Cyber Sunset T-Shirt Front View",
        "is_primary": true,
        "display_order": 0
      }
    ]
  }'
```

### 3. Query Products
```bash
# Get all products
curl http://localhost:8000/api/v1/products

# Get products by artist
curl http://localhost:8000/api/v1/products?artist_id=1

# Get featured products
curl http://localhost:8000/api/v1/products?featured=true

# Get specific product with details
curl http://localhost:8000/api/v1/products/1
```

## Database Management

### View Current Database
```bash
cd backend
sqlite3 y2k_shopping.db

# Inside SQLite:
.tables                  # List all tables
.schema users           # See user table structure
SELECT * FROM artists;  # Query artists
.quit                   # Exit
```

### Make Schema Changes

When you need to modify the database schema:

```bash
# 1. Update the model in app/models/
# For example, add a field to Product model

# 2. Generate migration
alembic revision --autogenerate -m "Add field to product"

# 3. Review the generated migration file
# Check alembic/versions/

# 4. Apply migration
alembic upgrade head

# 5. Rollback if needed
alembic downgrade -1
```

### Common Alembic Commands
```bash
# Show current migration version
alembic current

# Show migration history
alembic history

# Upgrade to latest
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>

# Reset database (downgrade all)
alembic downgrade base
```

## Next Steps

### 1. Add Authentication
Create `app/routes/auth.py` with JWT authentication:
- User registration
- Login/logout
- Password hashing with passlib
- Protected endpoints

### 2. Add Cart Endpoints
Create `app/routes/cart.py`:
- Add items to cart
- Update quantities
- Remove items
- Get cart summary

### 3. Add Order Processing
Create `app/routes/orders.py`:
- Create order from cart
- Update order status
- Track shipments
- Order history

### 4. Add Payment Integration
- Set up Stripe
- Create payment intent
- Handle webhooks
- Record payment status

### 5. Add Category Management
Create `app/routes/categories.py`:
- CRUD for categories
- Hierarchy support
- Product filtering by category

## Why This Schema is Robust

✅ **Product Variants** - Handle any combination of size/color/style
✅ **Inventory Tracking** - Per-variant stock with audit logs
✅ **Artist Commission** - Track commissions at order time
✅ **Order Snapshots** - Prices/names saved at purchase time
✅ **Flexible Addresses** - Multiple addresses per user
✅ **Digital + Physical** - Support both product types
✅ **Soft Deletes** - `is_active` flags preserve data
✅ **Extensible** - JSON fields for future flexibility
✅ **SEO Ready** - Slugs for URL-friendly identifiers

## Database Schema Highlights

### Product Variants Enable:
- Different sizes (XS, S, M, L, XL, XXL)
- Different colors per product
- Different styles (e.g., hoodie, t-shirt, tank)
- Individual pricing (sale prices, premium variants)
- Separate inventory tracking
- Different SKUs for each variant

### Order Snapshots Prevent:
- Historical orders showing wrong prices when products change
- Broken orders when products are deleted
- Commission calculation errors

### Artist System Supports:
- Commission tracking at order level
- Artist portfolios
- Featured artist promotion
- Social media integration
- Individual artist pages

## Resources

- **Database Schema**: See `DATABASE_SCHEMA.md`
- **API Documentation**: http://localhost:8000/api/v1/docs
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Alembic Tutorial**: https://alembic.sqlalchemy.org/
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **Pydantic Docs**: https://docs.pydantic.dev/

---

**Your e-commerce database is ready to use!** 🚀
