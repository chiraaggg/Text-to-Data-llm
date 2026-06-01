import sqlite3
import random
from datetime import datetime, timedelta

random.seed(42)

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Rehan", "Ayaan",
    "Krishna", "Ishaan", "Priya", "Ananya", "Divya", "Kavya", "Sneha", "Pooja",
    "Neha", "Riya", "Isha", "Meera", "Rahul", "Rohan", "Karan", "Nikhil", "Amit",
    "Vikram", "Suresh", "Rajesh", "Mahesh", "Ganesh", "Lakshmi", "Sunita", "Geeta",
    "Rekha", "Usha", "Harish", "Dinesh", "Ramesh", "Naresh", "Girish", "Anjali",
    "Deepika", "Shruti", "Tanvi", "Pallavi", "Siddharth", "Abhishek", "Kartik",
    "Manish", "Yogesh",
]

LAST_NAMES = [
    "Sharma", "Patel", "Singh", "Kumar", "Gupta", "Joshi", "Mehta", "Shah",
    "Verma", "Yadav", "Tiwari", "Mishra", "Pandey", "Dubey", "Chauhan",
    "Agarwal", "Goel", "Bansal", "Mittal", "Jain",
]

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata",
    "Ahmedabad", "Surat", "Jaipur", "Lucknow", "Kochi", "Indore", "Bhopal", "Nagpur",
]

CATEGORIES = [
    (1, "Fruits & Vegetables"),
    (2, "Dairy & Eggs"),
    (3, "Bakery & Snacks"),
    (4, "Beverages"),
    (5, "Meat & Seafood"),
    (6, "Frozen Foods"),
    (7, "Personal Care"),
    (8, "Household Essentials"),
]

ITEMS = [
    # Fruits & Vegetables
    (1,  "Fresh Tomatoes (1kg)",       1, 45.0,  "Farm fresh red tomatoes"),
    (2,  "Organic Bananas (dozen)",    1, 60.0,  "Organic Cavendish bananas"),
    (3,  "Spinach Bunch",              1, 30.0,  "Fresh green spinach"),
    (4,  "Potatoes (2kg)",             1, 55.0,  "Premium Agra potatoes"),
    (5,  "Onions (1kg)",               1, 40.0,  "Indian red onions"),
    (6,  "Apples (4 pcs)",             1, 120.0, "Himalayan Shimla apples"),
    (7,  "Green Peas (500g)",          1, 50.0,  "Fresh garden peas"),
    (8,  "Carrots (500g)",             1, 35.0,  "Organic baby carrots"),
    # Dairy & Eggs
    (9,  "Full Cream Milk (1L)",       2, 68.0,  "Amul full cream milk"),
    (10, "Greek Yogurt (400g)",        2, 95.0,  "Thick creamy yogurt"),
    (11, "Paneer (200g)",              2, 85.0,  "Fresh cottage cheese"),
    (12, "Butter (100g)",              2, 55.0,  "Amul salted butter"),
    (13, "Cheese Slices (10 pcs)",     2, 110.0, "Processed cheese slices"),
    (14, "Eggs (12 pcs)",              2, 90.0,  "Farm fresh eggs"),
    (15, "Curd (500g)",                2, 50.0,  "Dahi fresh curd"),
    (16, "Pure Cow Ghee (500ml)",      2, 280.0, "Traditional pure ghee"),
    # Bakery & Snacks
    (17, "Whole Wheat Bread",          3, 45.0,  "High-fiber bread loaf"),
    (18, "Digestive Biscuits (400g)",  3, 80.0,  "McVities digestive biscuits"),
    (19, "Lays Classic (80g)",         3, 30.0,  "Salted potato chips"),
    (20, "Butter Croissants (4 pcs)",  3, 120.0, "Flaky butter croissants"),
    (21, "Dark Chocolate (100g)",      3, 95.0,  "70% cocoa dark chocolate"),
    (22, "Granola Bars (6 pcs)",       3, 150.0, "Oats and honey bars"),
    (23, "Peanut Butter (350g)",       3, 175.0, "Creamy natural peanut butter"),
    (24, "Mixed Nuts (200g)",          3, 220.0, "Almonds, cashews, walnuts"),
    # Beverages
    (25, "Orange Juice (1L)",          4, 120.0, "100% pure orange juice"),
    (26, "Green Tea (25 bags)",        4, 90.0,  "Organic green tea"),
    (27, "Cold Coffee (250ml)",        4, 65.0,  "Ready-to-drink cold coffee"),
    (28, "Sparkling Water (1L)",       4, 50.0,  "Mineral sparkling water"),
    (29, "Coconut Water (300ml)",      4, 40.0,  "Natural tender coconut water"),
    (30, "Protein Shake (500ml)",      4, 180.0, "Chocolate whey protein"),
    (31, "Turmeric Latte Mix (200g)",  4, 220.0, "Golden milk powder blend"),
    (32, "Energy Drink (250ml)",       4, 75.0,  "Caffeine energy boost"),
    # Meat & Seafood
    (33, "Chicken Breast (500g)",      5, 185.0, "Boneless skinless chicken"),
    (34, "Salmon Fillet (200g)",       5, 350.0, "Norwegian Atlantic salmon"),
    (35, "Mutton Curry Cut (500g)",    5, 420.0, "Tender mutton pieces"),
    (36, "Tiger Prawns (250g)",        5, 280.0, "Deveined tiger prawns"),
    (37, "Tuna Can (185g)",            5, 140.0, "Skipjack tuna in water"),
    (38, "Fish Fingers (300g)",        5, 195.0, "Crispy battered fish fingers"),
    # Frozen Foods
    (39, "Frozen Peas (500g)",         6, 75.0,  "Garden peas flash frozen"),
    (40, "Veg Burger Patty (4 pcs)",   6, 160.0, "Plant-based burger patties"),
    (41, "Frozen Pizza (350g)",        6, 220.0, "Margherita stone-baked pizza"),
    (42, "Vanilla Ice Cream (500ml)",  6, 150.0, "Madagascar vanilla ice cream"),
    (43, "Frozen Parathas (5 pcs)",    6, 85.0,  "Whole wheat stuffed parathas"),
    (44, "Sweet Corn Kernels (500g)",  6, 65.0,  "Flash-frozen sweet corn"),
    # Personal Care
    (45, "Anti-Dandruff Shampoo (400ml)", 7, 225.0, "Zinc pyrithione shampoo"),
    (46, "Daily Moisturizer (150ml)",  7, 295.0, "SPF 30 daily moisturizer"),
    (47, "Whitening Toothpaste (150g)",7, 85.0,  "Advanced whitening toothpaste"),
    (48, "Hand Sanitizer (300ml)",     7, 120.0, "70% alcohol gel sanitizer"),
    (49, "Body Wash (250ml)",          7, 175.0, "Aloe vera shower gel"),
    (50, "Sunscreen SPF50 (100ml)",    7, 340.0, "Broad spectrum sunscreen"),
    # Household Essentials
    (51, "Lemon Dish Soap (500ml)",    8, 80.0,  "Grease-cutting dish liquid"),
    (52, "Floor Cleaner (1L)",         8, 130.0, "Disinfectant floor cleaner"),
    (53, "Laundry Detergent (1kg)",    8, 195.0, "Front-load washing powder"),
    (54, "Toilet Cleaner (500ml)",     8, 95.0,  "Limescale toilet cleaner"),
    (55, "Kitchen Paper Towels (2 pk)",8, 120.0, "Absorbent paper towels"),
    (56, "Garbage Bags (30 pcs)",      8, 85.0,  "Large 60L garbage bags"),
]

ORDER_STATUSES = ["pending", "confirmed", "delivering", "delivered", "cancelled"]
PAYMENT_METHODS = ["upi", "card", "cash", "wallet"]


def _rand_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def create_demo_db(db_path: str = "demo.db") -> None:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id   INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS items (
            id          INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            category_id INTEGER REFERENCES categories(id),
            price       REAL NOT NULL,
            description TEXT
        );
        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER PRIMARY KEY,
            name       TEXT NOT NULL,
            email      TEXT UNIQUE,
            phone      TEXT,
            city       TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS orders (
            id         INTEGER PRIMARY KEY,
            user_id    INTEGER REFERENCES users(id),
            status     TEXT NOT NULL,
            created_at TEXT NOT NULL,
            city       TEXT
        );
        CREATE TABLE IF NOT EXISTS order_items (
            id       INTEGER PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id),
            item_id  INTEGER REFERENCES items(id),
            quantity INTEGER NOT NULL,
            price    REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS order_payments (
            id             INTEGER PRIMARY KEY,
            order_id       INTEGER REFERENCES orders(id),
            amount         REAL NOT NULL,
            status         TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            created_at     TEXT NOT NULL
        );
    """)

    c.executemany("INSERT OR IGNORE INTO categories VALUES (?, ?)", CATEGORIES)
    c.executemany(
        "INSERT OR IGNORE INTO items VALUES (?, ?, ?, ?, ?)", ITEMS
    )

    # --- Users (150) ---
    end_date   = datetime(2026, 6, 1)
    start_date = datetime(2025, 1, 1)

    users = []
    used_emails: set = set()
    for uid in range(1, 151):
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        base_email = f"{fn.lower()}.{ln.lower()}{uid}@example.com"
        while base_email in used_emails:
            base_email = f"{fn.lower()}.{ln.lower()}{uid}_{random.randint(1,99)}@example.com"
        used_emails.add(base_email)
        phone = f"+91 9{random.randint(100000000, 999999999)}"
        city  = random.choice(CITIES)
        reg   = _rand_date(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S")
        users.append((uid, f"{fn} {ln}", base_email, phone, city, reg))

    c.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)", users)

    # --- Orders (900) ---
    order_start = datetime(2025, 6, 1)
    orders, order_items_rows, payments = [], [], []
    oi_id, pay_id = 1, 1

    for oid in range(1, 901):
        user = random.choice(users)
        uid, _, _, _, user_city, _ = user

        order_dt = _rand_date(order_start, end_date)
        age_days  = (end_date - order_dt).days

        # Older orders → more likely delivered
        if age_days > 14:
            status = random.choices(
                ORDER_STATUSES, weights=[2, 5, 3, 80, 10]
            )[0]
        elif age_days > 5:
            status = random.choices(
                ORDER_STATUSES, weights=[10, 20, 25, 35, 10]
            )[0]
        else:
            status = random.choices(
                ORDER_STATUSES, weights=[40, 30, 20, 5, 5]
            )[0]

        orders.append((oid, uid, status, order_dt.strftime("%Y-%m-%d %H:%M:%S"), user_city))

        # --- Order items (1-5 per order) ---
        n_items   = random.randint(1, 5)
        chosen    = random.sample(ITEMS, n_items)
        order_total = 0.0
        for item in chosen:
            iid, _, _, item_price, _ = item
            qty   = random.randint(1, 3)
            price = round(item_price * qty, 2)
            order_total += price
            order_items_rows.append((oi_id, oid, iid, qty, price))
            oi_id += 1

        # --- Payment ---
        if status == "cancelled" and random.random() < 0.65:
            continue  # most cancelled orders never reach payment

        if status == "delivered":
            pay_status = "success"
        elif status == "cancelled":
            pay_status = "failed"
        else:
            pay_status = "pending"

        method = random.choices(
            PAYMENT_METHODS, weights=[55, 25, 10, 10]
        )[0]
        pay_dt = (order_dt + timedelta(minutes=random.randint(1, 10))).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        payments.append((pay_id, oid, round(order_total, 2), pay_status, method, pay_dt))
        pay_id += 1

    c.executemany("INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?, ?)", orders)
    c.executemany(
        "INSERT OR IGNORE INTO order_items VALUES (?, ?, ?, ?, ?)", order_items_rows
    )
    c.executemany(
        "INSERT OR IGNORE INTO order_payments VALUES (?, ?, ?, ?, ?, ?)", payments
    )

    conn.commit()
    conn.close()
    print(f"Demo DB created at '{db_path}' — {len(users)} users, {len(orders)} orders.")


if __name__ == "__main__":
    create_demo_db()
