import pandas as pd
import random

# 1. Category examples with "Check" entries added to Accounts Receivable
category_samples = {
    "Accounts Receivable": [
        "Zelle from John Doe", "Venmo Payment", "Cash App Transfer", "Square Deposit",
        "PayPal Business", "DoorDash Driver Pay", "Uber Payout", "Stripe Transfer",
        "Client Check", "Check", "Received Check"
    ],
    "Automobile Expense": [
        "ExxonMobil Fuel", "Shell Oil Gas", "Valvoline Oil Change", "AutoZone Parts",
        "Sunoco Gas", "Jiffy Lube Service", "Firestone Tires", "Wawa Fuel Station"
    ],
    "Dues and Subscriptions": [
        "Spotify Subscription", "Netflix Monthly Fee", "Adobe Creative Cloud",
        "Google Workspace", "YouTube Premium", "Intuit QuickBooks", "Amazon Prime", "Dropbox Plan"
    ],
    "Food Purchases": [
        "Walmart Grocery", "Whole Foods Market", "Trader Joe's", "McDonald's", "Chick-fil-A",
        "Popeyes Chicken", "Starbucks Coffee", "Giant Food Store"
    ],
    "Insurance Expense": [
        "Geico Auto Insurance", "State Farm Policy", "Progressive Insurance",
        "Allstate Premium", "Liberty Mutual Auto", "Farmers Insurance"
    ],
    "Office Supplies": [
        "Staples Office Depot", "Amazon Office Desk", "Best Buy Monitor",
        "Walmart Printer Ink", "OfficeMax Paper Supplies", "Target Office Chair"
    ],
    "Professional Fees": [
        "LegalZoom Service", "H&R Block Tax Filing", "CPA Tax Prep", "Consulting Fee - Tech",
        "Bookkeeping Service", "Freelance Developer"
    ],
    "Repairs and Maintenance": [
        "Home Depot Repairs", "Lowe's Maintenance", "Plumber Joe's Service", "Electrician Service",
        "HVAC Tune-Up", "Contractor Payment", "Handyman Fee"
    ],
    "Computer and Internet Expense": [
        "Comcast Internet", "AT&T Fiber", "T-Mobile 5G Plan", "Verizon Hotspot", "Zoom Pro Account",
        "Microsoft 365 Subscription"
    ],
    "Merchant Account Fees": [
        "Square Transaction Fee", "Stripe Processing", "PayPal Fee", "Shopify Payout Fee",
        "Etsy Transaction Fee", "Intuit Merchant Fee"
    ]
}

# 2. Dataset generator function
def generate_dataset(samples_per_class=1000):
    data = []
    for category, examples in category_samples.items():
        for _ in range(samples_per_class):
            base = random.choice(examples)

            # Inject realistic check numbers for "check" descriptions
            if category == "Accounts Receivable" and "check" in base.lower():
                base = f"{base} #{random.randint(1000, 9999)}"

            # Add random noise and formatting variants
            noise = random.choice([
                f"{base} #{random.randint(1000,9999)}",
                f"{base} - {random.choice(['TX', 'NY', 'CA'])}",
                f"{base} ({random.randint(1, 12)}/{random.randint(1, 28)}/2025)",
                f"{base} {random.choice(['Online', 'In-store'])}",
                f"{base}"
            ])

            amount = round(random.uniform(5.00, 500.00), 2)
            txn_type = "Credit" if category == "Accounts Receivable" else "Debit"

            data.append({
                "Description": noise,
                "Amount": amount if txn_type == "Credit" else -amount,
                "Type": txn_type,
                "Account": category
            })
    return pd.DataFrame(data)

# 3. Generate and save the dataset
if __name__ == "__main__":
    df = generate_dataset(samples_per_class=1000)
    df.to_csv("Sorting_Data.csv", index=False)
    print("Saved as Sorting_Data.csv with", df.shape[0], "rows")
