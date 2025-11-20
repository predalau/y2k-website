"""
Seed script to populate database with mock data for AEVVM store
"""
import sys
from datetime import datetime, timedelta
import random
from decimal import Decimal

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.artist import Artist
from app.models.category import Category
from app.models.product import Product, ProductVariant, ProductImage
from app.models.address import Address
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.review import Review

def get_password_hash(password):
    """Simple hash for demo purposes - in production use proper bcrypt"""
    # For demo purposes, just use a simple hash
    # In real app, use proper password hashing
    return f"hashed_{password}"

def create_mock_data():
    """Create comprehensive mock data"""
    db = SessionLocal()

    try:
        print("🔨 Starting database seeding...")

        # Clear existing data (optional)
        print("  Clearing existing data...")
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()

        # 1. Create Users
        print("  Creating users...")
        admin = User(
            email="admin@aevvm.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            phone="555-0100",
            is_active=True,
            is_admin=True,
            email_verified=True
        )
        db.add(admin)

        users = []
        user_names = [
            ("Alice", "Johnson", "alice.j@email.com", "555-0101"),
            ("Bob", "Smith", "bob.smith@email.com", "555-0102"),
            ("Carol", "Davis", "carol.d@email.com", "555-0103"),
            ("David", "Wilson", "david.w@email.com", "555-0104"),
            ("Emma", "Brown", "emma.b@email.com", "555-0105"),
            ("Frank", "Miller", "frank.m@email.com", "555-0106"),
            ("Grace", "Taylor", "grace.t@email.com", "555-0107"),
            ("Henry", "Anderson", "henry.a@email.com", "555-0108"),
            ("Iris", "Thomas", "iris.t@email.com", "555-0109"),
            ("Jack", "Martinez", "jack.m@email.com", "555-0110"),
        ]

        for first, last, email, phone in user_names:
            user = User(
                email=email,
                hashed_password=get_password_hash("password123"),
                full_name=f"{first} {last}",
                phone=phone,
                is_active=True,
                is_admin=False,
                email_verified=random.choice([True, False])
            )
            users.append(user)
            db.add(user)

        db.commit()
        print(f"    ✓ Created {len(users) + 1} users")

        # 2. Create Categories
        print("  Creating categories...")
        categories_data = [
            ("T-Shirts", "tshirts", "Classic Y2K style t-shirts"),
            ("Hoodies", "hoodies", "Cozy hoodies with retro designs"),
            ("Stickers", "stickers", "Vinyl stickers for laptops and phones"),
            ("Posters", "posters", "Art prints and posters"),
            ("Accessories", "accessories", "Pins, patches, and more")
        ]

        categories = []
        for name, slug, desc in categories_data:
            category = Category(
                name=name,
                slug=slug,
                description=desc,
                is_active=True
            )
            categories.append(category)
            db.add(category)

        db.commit()
        print(f"    ✓ Created {len(categories)} categories")

        # 3. Create Artists
        print("  Creating artists...")
        artists_data = [
            ("Sarah Chen", "sarah-chen", "Minimalist brutalist designer", 15.0, True),
            ("Mike Torres", "mike-torres", "Industrial typography specialist", 12.0, True),
            ("Luna Park", "luna-park", "Concrete structure artist", 18.0, True),
            ("Alex Rivera", "alex-rivera", "Raw architectural designer", 10.0, False),
            ("Jamie Kim", "jamie-kim", "Chrome metallic sculptor", 20.0, True),
        ]

        artists = []
        for name, slug, bio, commission, featured in artists_data:
            artist = Artist(
                name=name,
                slug=slug,
                bio=bio,
                commission_rate=Decimal(str(commission)),
                is_active=True,
                featured=featured,
                instagram=f"@{slug.replace('-', '_')}",
                twitter=f"@{slug.replace('-', '')}"
            )
            artists.append(artist)
            db.add(artist)

        db.commit()
        print(f"    ✓ Created {len(artists)} artists")

        # 4. Create Products with Variants
        print("  Creating products...")
        products_data = [
            ("Concrete Form T-Shirt", "concrete-form-tshirt", "Heavy cotton with brutalist geometry", 29.99, "physical", 0, 0),
            ("Steel Structure Hoodie", "steel-structure-hoodie", "Industrial weight fleece", 59.99, "physical", 0, 1),
            ("Chrome Decal Pack", "chrome-decal-stickers", "Set of 10 metallic vinyl stickers", 12.99, "physical", 2, 0),
            ("Brutalist Grid Poster", "brutalist-poster", "Museum-grade architectural print", 24.99, "physical", 3, 1),
            ("Industrial Pin Set", "industrial-pins", "Brushed steel enamel pins", 19.99, "physical", 4, 2),
            ("Digital Asset Pack", "digital-assets", "10 4K brutalist wallpapers", 9.99, "digital", 3, 3),
            ("Raw Form Tee", "raw-form-tee", "Monochrome structural design", 27.99, "physical", 0, 1),
            ("Chrome Void Hoodie", "chrome-void-hoodie", "Reflective metallic print", 64.99, "physical", 0, 4),
        ]

        products = []
        for name, slug, desc, price, ptype, cat_idx, artist_idx in products_data:
            product = Product(
                name=name,
                slug=slug,
                description=desc,
                short_description=desc[:50],
                product_type=ptype,
                base_price=Decimal(str(price)),
                is_active=True,
                featured=random.choice([True, False]),
                artist_id=artists[artist_idx].id,
                category_id=categories[cat_idx].id if cat_idx < len(categories) else None
            )
            products.append(product)
            db.add(product)

        db.commit()

        # Add variants for physical products
        sizes = ['S', 'M', 'L', 'XL']
        colors = ['Black', 'White', 'Navy', 'Grey']

        variant_count = 0
        for product in products:
            if product.product_type == 'physical':
                # Add 4-8 variants per product
                num_variants = random.randint(4, 8)
                for i in range(num_variants):
                    size = random.choice(sizes)
                    color = random.choice(colors)
                    variant = ProductVariant(
                        product_id=product.id,
                        sku=f"{product.slug[:10].upper()}-{size}-{color[:3].upper()}-{i}",
                        name=f"{size} - {color}",
                        size=size,
                        color=color,
                        price=product.base_price + Decimal(str(random.uniform(-5, 5))),
                        stock_quantity=random.randint(10, 100),
                        low_stock_threshold=5,
                        track_inventory=True,
                        is_active=True,
                        display_order=i
                    )
                    db.add(variant)
                    variant_count += 1
            else:
                # Digital product - single variant
                variant = ProductVariant(
                    product_id=product.id,
                    sku=f"{product.slug[:10].upper()}-DIGITAL",
                    name="Digital Download",
                    price=product.base_price,
                    stock_quantity=9999,
                    track_inventory=False,
                    requires_shipping=False,
                    is_active=True
                )
                db.add(variant)
                variant_count += 1

        db.commit()
        print(f"    ✓ Created {len(products)} products with {variant_count} variants")

        # 5. Create Addresses for users
        print("  Creating addresses...")
        addresses = []
        for user in users[:5]:  # Only first 5 users have addresses
            address = Address(
                user_id=user.id,
                address_type="both",
                full_name=user.full_name,
                phone=user.phone,
                address_line1=f"{random.randint(100, 9999)} Main St",
                city=random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
                state=random.choice(["NY", "CA", "IL", "TX", "AZ"]),
                postal_code=f"{random.randint(10000, 99999)}",
                country="USA",
                is_default=True
            )
            addresses.append(address)
            db.add(address)

        db.commit()
        print(f"    ✓ Created {len(addresses)} addresses")

        # 6. Create Orders with realistic dates
        print("  Creating orders...")
        order_statuses = ['paid', 'processing', 'shipped', 'delivered', 'pending', 'cancelled']
        order_status_weights = [30, 20, 15, 25, 8, 2]  # Most orders are completed

        orders = []
        order_items_list = []

        # Create orders over last 60 days
        for i in range(50):
            user = random.choice(users)
            days_ago = random.randint(0, 60)
            order_date = datetime.now() - timedelta(days=days_ago)

            status = random.choices(order_statuses, weights=order_status_weights)[0]

            # Get variants for this order (1-4 items)
            all_variants = db.query(ProductVariant).filter(ProductVariant.is_active == True).all()
            order_variants = random.sample(all_variants, random.randint(1, 4))

            subtotal = Decimal('0.00')
            order_items = []

            for variant in order_variants:
                product = db.query(Product).filter(Product.id == variant.product_id).first()
                artist = db.query(Artist).filter(Artist.id == product.artist_id).first()

                quantity = random.randint(1, 3)
                item_subtotal = variant.price * quantity
                subtotal += item_subtotal

                order_item = OrderItem(
                    variant_id=variant.id,
                    artist_id=artist.id,
                    product_name=product.name,
                    variant_name=variant.name,
                    sku=variant.sku,
                    price=variant.price,
                    quantity=quantity,
                    subtotal=item_subtotal,
                    artist_commission_rate=artist.commission_rate
                )
                order_items.append(order_item)

            tax_amount = subtotal * Decimal('0.08')  # 8% tax
            shipping_amount = Decimal('5.99') if any(v.requires_shipping for v in order_variants) else Decimal('0.00')
            total_amount = subtotal + tax_amount + shipping_amount

            # Get or create address
            address = None
            if addresses:
                address = random.choice(addresses)

            order = Order(
                user_id=user.id,
                order_number=f"AEV-{1000 + i}",
                status=status,
                subtotal=subtotal,
                tax_amount=tax_amount,
                shipping_amount=shipping_amount,
                discount_amount=Decimal('0.00'),
                total_amount=total_amount,
                currency="USD",
                shipping_address_id=address.id if address else None,
                billing_address_id=address.id if address else None,
                customer_email=user.email,
                customer_phone=user.phone,
                created_at=order_date
            )

            # Add shipped/delivered dates for completed orders
            if status in ['shipped', 'delivered']:
                order.shipped_at = order_date + timedelta(days=random.randint(1, 3))
                order.tracking_number = f"TRK{random.randint(100000000, 999999999)}"

            if status == 'delivered':
                order.delivered_at = order.shipped_at + timedelta(days=random.randint(2, 7))

            orders.append(order)
            db.add(order)
            db.flush()  # Get order ID

            # Add order items
            for item in order_items:
                item.order_id = order.id
                db.add(item)
                order_items_list.append(item)

            # Create payment for paid orders
            if status in ['paid', 'processing', 'shipped', 'delivered']:
                payment = Payment(
                    order_id=order.id,
                    payment_method="stripe",
                    transaction_id=f"ch_{random.randint(1000000000, 9999999999)}",
                    amount=total_amount,
                    currency="USD",
                    status="completed",
                    paid_at=order_date
                )
                db.add(payment)

        db.commit()
        print(f"    ✓ Created {len(orders)} orders with {len(order_items_list)} items")

        # 7. Create Reviews
        print("  Creating reviews...")
        reviews = []
        delivered_orders = [o for o in orders if o.status == 'delivered']
        reviewed_products = set()  # Track (user_id, product_id) to avoid duplicates

        for order in random.sample(delivered_orders, min(15, len(delivered_orders))):
            order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

            for item in random.sample(order_items, min(2, len(order_items))):
                product = db.query(Product).filter(Product.id == item.variant.product_id).first()

                # Check if user already reviewed this product
                review_key = (order.user_id, product.id)
                if review_key in reviewed_products:
                    continue

                reviewed_products.add(review_key)

                review = Review(
                    product_id=product.id,
                    user_id=order.user_id,
                    order_item_id=item.id,
                    rating=random.randint(3, 5),
                    title=random.choice([
                        "Love it!", "Great quality", "Amazing design",
                        "Perfect fit", "Exceeded expectations"
                    ]),
                    comment=random.choice([
                        "The quality is outstanding and the design is exactly what I wanted!",
                        "Fast shipping and great customer service. Highly recommend!",
                        "Perfect addition to my collection. Will buy again!",
                        "The material quality is exceptional and feels premium.",
                        "Exactly as pictured. Very happy with my purchase!"
                    ]),
                    is_verified_purchase=True,
                    is_approved=True,
                    created_at=order.delivered_at + timedelta(days=random.randint(1, 10))
                )
                reviews.append(review)
                db.add(review)

        db.commit()
        print(f"    ✓ Created {len(reviews)} reviews")

        print("\n✅ Database seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"   - Users: {len(users) + 1} (including 1 admin)")
        print(f"   - Artists: {len(artists)}")
        print(f"   - Categories: {len(categories)}")
        print(f"   - Products: {len(products)}")
        print(f"   - Product Variants: {variant_count}")
        print(f"   - Addresses: {len(addresses)}")
        print(f"   - Orders: {len(orders)}")
        print(f"   - Order Items: {len(order_items_list)}")
        print(f"   - Reviews: {len(reviews)}")
        print("\n🔑 Admin login:")
        print("   Email: admin@aevvm.com")
        print("   Password: admin123")

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🔨 AEVVM Store - Database Seed Script")
    print("=" * 50)

    response = input("\n⚠️  This will DELETE all existing data. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Seeding cancelled.")
        sys.exit(0)

    create_mock_data()
    print("\n🎉 Ready to test the admin dashboard at http://localhost:5173/admin/dashboard")
