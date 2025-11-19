# Database Schema Design - Artist Merch E-commerce

## Overview
Robust schema designed for selling artist-designed merchandise with support for:
- Multiple artists with profiles and portfolios
- Product variants (sizes, colors, styles)
- Inventory tracking per variant
- Digital and physical products
- Order management with status tracking
- Reviews and ratings
- Multiple product images
- Shipping addresses
- Payment records

## Entity Relationship Diagram

```
User (Customer/Admin)
├── addresses (1:many)
├── cart_items (1:many)
├── orders (1:many)
└── reviews (1:many)

Artist
├── products (1:many)
└── artist_images (1:many)

Product
├── artist (many:1)
├── category (many:1)
├── variants (1:many)
├── images (1:many)
└── reviews (1:many)

ProductVariant
├── product (many:1)
└── inventory records

Order
├── user (many:1)
├── shipping_address (many:1)
├── billing_address (many:1)
├── order_items (1:many)
└── payment (1:1)

OrderItem
├── order (many:1)
└── product_variant (many:1)
```

## Tables

### 1. users
Primary user authentication and profile.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| email | String(255) | Unique, Not Null, Index | |
| hashed_password | String(255) | Not Null | |
| full_name | String(255) | Nullable | |
| phone | String(50) | Nullable | |
| is_active | Boolean | Default True | Soft delete support |
| is_admin | Boolean | Default False | Admin privileges |
| email_verified | Boolean | Default False | Email verification |
| created_at | DateTime | Default now() | |
| updated_at | DateTime | Auto-update | |

### 2. artists
Local artists who design merchandise.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| name | String(255) | Not Null, Index | Artist/brand name |
| slug | String(255) | Unique, Index | URL-friendly identifier |
| bio | Text | Nullable | Artist description |
| profile_image_url | String(500) | Nullable | Main profile image |
| banner_image_url | String(500) | Nullable | Cover/banner image |
| website | String(500) | Nullable | Artist's website |
| instagram | String(255) | Nullable | Social media handle |
| twitter | String(255) | Nullable | Social media handle |
| commission_rate | Decimal(5,2) | Default 0.00 | % commission (0-100) |
| is_active | Boolean | Default True | Can be deactivated |
| featured | Boolean | Default False | Featured on homepage |
| created_at | DateTime | Default now() | |
| updated_at | DateTime | Auto-update | |

### 3. categories
Product categorization (flexible hierarchy).

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| name | String(255) | Not Null, Index | Category name |
| slug | String(255) | Unique, Index | URL-friendly |
| description | Text | Nullable | |
| parent_id | Integer | FK→categories.id, Nullable | For subcategories |
| image_url | String(500) | Nullable | Category image |
| display_order | Integer | Default 0 | For sorting |
| is_active | Boolean | Default True | |
| created_at | DateTime | Default now() | |

### 4. products
Main product information (design/concept).

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| artist_id | Integer | FK→artists.id, Not Null, Index | |
| category_id | Integer | FK→categories.id, Nullable, Index | |
| name | String(255) | Not Null, Index | Product name |
| slug | String(255) | Unique, Index | URL-friendly |
| description | Text | Nullable | Full description |
| short_description | String(500) | Nullable | Summary |
| product_type | String(50) | Not Null | 'physical', 'digital', 'both' |
| digital_file_url | String(500) | Nullable | For digital products |
| base_price | Decimal(10,2) | Not Null | Starting price (reference) |
| is_active | Boolean | Default True | Published/unpublished |
| featured | Boolean | Default False | Featured products |
| created_at | DateTime | Default now() | |
| updated_at | DateTime | Auto-update | |

### 5. product_variants
Specific variants (size, color, style) with individual pricing and inventory.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| product_id | Integer | FK→products.id, Not Null, Index | |
| sku | String(100) | Unique, Not Null, Index | Stock keeping unit |
| name | String(255) | Not Null | e.g., "Medium - Black" |
| size | String(50) | Nullable | S, M, L, XL, etc. |
| color | String(100) | Nullable | Color name |
| style | String(100) | Nullable | Any other variant dimension |
| price | Decimal(10,2) | Not Null | Actual selling price |
| compare_at_price | Decimal(10,2) | Nullable | Original price (for sales) |
| cost | Decimal(10,2) | Nullable | Cost to produce (internal) |
| weight | Decimal(8,2) | Nullable | For shipping (grams) |
| requires_shipping | Boolean | Default True | Physical vs digital |
| stock_quantity | Integer | Default 0 | Current inventory |
| low_stock_threshold | Integer | Default 5 | Alert threshold |
| track_inventory | Boolean | Default True | Enable inventory tracking |
| is_active | Boolean | Default True | Available for sale |
| display_order | Integer | Default 0 | Sort order |
| created_at | DateTime | Default now() | |
| updated_at | DateTime | Auto-update | |

### 6. product_images
Multiple images per product (separate from variants for flexibility).

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| product_id | Integer | FK→products.id, Not Null, Index | |
| image_url | String(500) | Not Null | Image URL/path |
| alt_text | String(255) | Nullable | Accessibility |
| display_order | Integer | Default 0 | Sort order |
| is_primary | Boolean | Default False | Main product image |
| created_at | DateTime | Default now() | |

### 7. addresses
Shipping and billing addresses (separate from users for flexibility).

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| user_id | Integer | FK→users.id, Not Null, Index | |
| address_type | String(50) | Not Null | 'shipping', 'billing', 'both' |
| full_name | String(255) | Not Null | Recipient name |
| phone | String(50) | Nullable | Contact number |
| address_line1 | String(255) | Not Null | Street address |
| address_line2 | String(255) | Nullable | Apt/Suite |
| city | String(100) | Not Null | |
| state | String(100) | Not Null | State/Province |
| postal_code | String(20) | Not Null | ZIP/Postal code |
| country | String(100) | Not Null | Country name |
| is_default | Boolean | Default False | Default address |
| created_at | DateTime | Default now() | |
| updated_at | DateTime | Auto-update | |

### 8. cart_items
Shopping cart (persisted to database).

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| user_id | Integer | FK→users.id, Not Null, Index | |
| variant_id | Integer | FK→product_variants.id, Not Null | |
| quantity | Integer | Not Null, Min 1 | |
| created_at | DateTime | Default now() | |
| updated_at | DateTime | Auto-update | |
| **Unique Constraint:** (user_id, variant_id) | | | Prevent duplicates |

### 9. orders
Customer orders.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| user_id | Integer | FK→users.id, Not Null, Index | |
| order_number | String(50) | Unique, Not Null, Index | Human-readable ID |
| status | String(50) | Not Null, Index | See status enum below |
| subtotal | Decimal(10,2) | Not Null | Before tax/shipping |
| tax_amount | Decimal(10,2) | Default 0.00 | Sales tax |
| shipping_amount | Decimal(10,2) | Default 0.00 | Shipping cost |
| discount_amount | Decimal(10,2) | Default 0.00 | Discounts applied |
| total_amount | Decimal(10,2) | Not Null | Final total |
| currency | String(3) | Default 'USD' | ISO currency code |
| shipping_address_id | Integer | FK→addresses.id, Nullable | Snapshot at order time |
| billing_address_id | Integer | FK→addresses.id, Nullable | |
| customer_email | String(255) | Not Null | Email at order time |
| customer_phone | String(50) | Nullable | Phone at order time |
| notes | Text | Nullable | Customer notes |
| admin_notes | Text | Nullable | Internal notes |
| tracking_number | String(255) | Nullable | Shipping tracking |
| shipped_at | DateTime | Nullable | When shipped |
| delivered_at | DateTime | Nullable | When delivered |
| cancelled_at | DateTime | Nullable | When cancelled |
| created_at | DateTime | Default now() | Order placed |
| updated_at | DateTime | Auto-update | |

**Order Status Enum:**
- `pending` - Order created, payment pending
- `paid` - Payment confirmed
- `processing` - Being prepared
- `shipped` - In transit
- `delivered` - Completed
- `cancelled` - Cancelled
- `refunded` - Refunded

### 10. order_items
Items within an order (snapshot of product data).

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| order_id | Integer | FK→orders.id, Not Null, Index | |
| variant_id | Integer | FK→product_variants.id, Not Null | Reference only |
| artist_id | Integer | FK→artists.id, Nullable | For commission calc |
| product_name | String(255) | Not Null | Snapshot |
| variant_name | String(255) | Not Null | Snapshot |
| sku | String(100) | Not Null | Snapshot |
| price | Decimal(10,2) | Not Null | Price at purchase time |
| quantity | Integer | Not Null | |
| subtotal | Decimal(10,2) | Not Null | price × quantity |
| artist_commission_rate | Decimal(5,2) | Nullable | Rate at purchase time |
| created_at | DateTime | Default now() | |

### 11. payments
Payment records.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| order_id | Integer | FK→orders.id, Unique, Not Null | One payment per order |
| payment_method | String(50) | Not Null | 'stripe', 'paypal', etc. |
| transaction_id | String(255) | Unique, Nullable | External payment ID |
| amount | Decimal(10,2) | Not Null | Amount charged |
| currency | String(3) | Default 'USD' | |
| status | String(50) | Not Null | See status enum below |
| payment_data | JSON | Nullable | Raw payment response |
| paid_at | DateTime | Nullable | Payment confirmed time |
| refunded_at | DateTime | Nullable | Refund time |
| created_at | DateTime | Default now() | |
| updated_at | DateTime | Auto-update | |

**Payment Status Enum:**
- `pending` - Initiated
- `completed` - Successful
- `failed` - Failed
- `refunded` - Refunded
- `cancelled` - Cancelled

### 12. reviews
Product reviews and ratings.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| product_id | Integer | FK→products.id, Not Null, Index | |
| user_id | Integer | FK→users.id, Not Null, Index | |
| order_item_id | Integer | FK→order_items.id, Nullable | Verified purchase |
| rating | Integer | Not Null | 1-5 stars |
| title | String(255) | Nullable | Review headline |
| comment | Text | Nullable | Review text |
| is_verified_purchase | Boolean | Default False | Bought this item |
| is_approved | Boolean | Default True | Moderation |
| helpful_count | Integer | Default 0 | Upvotes |
| created_at | DateTime | Default now() | |
| updated_at | DateTime | Auto-update | |
| **Unique Constraint:** (product_id, user_id) | | | One review per product per user |

### 13. inventory_logs (Optional but recommended)
Track inventory changes for auditing.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto | |
| variant_id | Integer | FK→product_variants.id, Not Null, Index | |
| change_type | String(50) | Not Null | 'sale', 'restock', 'adjustment', 'return' |
| quantity_change | Integer | Not Null | Positive or negative |
| quantity_after | Integer | Not Null | Stock after change |
| reference_id | Integer | Nullable | Order ID or other reference |
| notes | String(500) | Nullable | Reason for change |
| created_by | Integer | FK→users.id, Nullable | Admin who made change |
| created_at | DateTime | Default now() | |

## Indexes Summary

**Critical indexes for performance:**
- users: email, created_at
- artists: slug, is_active, featured
- categories: slug, parent_id
- products: artist_id, category_id, slug, is_active, featured
- product_variants: product_id, sku, is_active
- product_images: product_id
- addresses: user_id
- cart_items: user_id, (user_id, variant_id) unique
- orders: user_id, order_number, status, created_at
- order_items: order_id, variant_id
- payments: order_id, transaction_id, status
- reviews: product_id, user_id
- inventory_logs: variant_id, created_at

## Why This Schema is Robust

1. **Product Variants**: Handles any combination of size/color/style with individual pricing and inventory
2. **Artist Separation**: Artists are first-class entities with their own profiles and commission tracking
3. **Order Snapshots**: Order items store product info at purchase time (price, name, etc.) so historical orders remain accurate even if products change
4. **Flexible Addresses**: Addresses are separate entities, supporting multiple addresses per user
5. **Digital + Physical**: Product type field and variant shipping requirements support both
6. **Inventory Tracking**: Optional per-variant with audit logs
7. **Payment Abstraction**: Supports multiple payment providers
8. **Review System**: Verified purchases, moderation, helpful counts
9. **Soft Deletes**: is_active flags instead of hard deletes preserve referential integrity
10. **Extensibility**: JSON fields for future flexibility, slugs for SEO, display_order for custom sorting

## Migration Strategy

1. Create all models
2. Set up Alembic
3. Generate initial migration
4. Add seed data for categories and test artists
5. Test with sample products
6. Add indexes after initial data load for better performance
