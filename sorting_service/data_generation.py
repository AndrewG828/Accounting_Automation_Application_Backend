import pandas as pd
import random

# Updated account categories and description samples
description_samples_by_account = {
    "Accounts Receivable": [
        "DoorDash, INC. DES: DoorDash", "Uber Payout", "Stripe Transfer", "Merchant Bankcd", "Grubhub"
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
        "Walmart Grocery", "Whole Foods Market", "Trader Joe's", "Giant Food Store", "WISMETTAC ASIAN", "Sysco Corporatio"
    ],
    "Meals and Entertainment": [
        "McDonald's", "Chick-fil-A", "Popeyes Chicken", "Starbucks Coffee", "Judy's Sichuan"
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
        "Bookkeeping Service", "Freelance Developer", "MDG Tax and Accounting Services", "Adoluna"
    ],
    "Repairs and Maintenance": [
        "Home Depot Repairs", "Lowe's Maintenance", "Plumber Joe's Service", "Electrician Service",
        "HVAC Tune-Up", "Contractor Payment", "Handyman Fee", "AUTO CHLOR NVA"
    ],
    "Computer and Internet Expense": [
        "Comcast Internet", "AT&T Fiber", "T-Mobile 5G Plan", "Verizon Hotspot", "Zoom Pro Account",
        "Microsoft 365 Subscription"
    ],
    "Merchant Account Fees": [
        "Square Transaction Fee", "Stripe Processing", "Shopify Payout Fee",
        "Etsy Transaction Fee", "Intuit Merchant Fee", "Merchant BankCD"
    ],
    "Bank Service Charges": [
        "Excess Transaction Fee"
    ],
    "Other Income": [
        "Bank of America"
    ]
}

# Function to generate the dataset
def generate_synthetic_data(samples_per_account=1000):
    data = []
    for account, descriptions in description_samples_by_account.items():
        for _ in range(samples_per_account):
            description = random.choice(descriptions)
            amount = round(random.uniform(10.00, 5000.00), 2)
            # Income categories
            if account == "Accounts Receivable":
                signed_amount = amount
            else:
                signed_amount = -amount
            data.append({
                "Description": description,
                "Amount": signed_amount,
                "Account": account
            })
    return pd.DataFrame(data)

# Save to CSV
if __name__ == "__main__":
    df = generate_synthetic_data(samples_per_account=1000)
    df.to_csv("Sorting_Data.csv", index=False)
    print("Saved as 'Sorting_Data' with", df.shape[0], "rows")
