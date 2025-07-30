# 💳 CC-KILLER

A powerful card testing utility made for **educational and security research purposes only**.  
Supports **multiple payment gateways** to simulate card decline mechanisms and "kill" compromised credit cards using valid + fake charge techniques.

> ⚠️ Developer: **Tawhed**  
> ❗ You must **add your own API credentials** before use  
> ☠️ For **educational use only** — use responsibly

---

## 📁 Structure

```bash
CC-KILLER/
├── launcher.sh                # Main launcher script
└── module/
    ├── STRIPE_KILLER.py
    ├── PAYPAL_KILLER.py
    ├── SQUARE_KILLER.py
    ├── BRAINTREE_KILLER.py
    ├── AUTHORIZE_KILLER.py
    └── SSLCommerz_KILLER.py
```

Each module targets a different payment gateway and includes its own API logic.

---

## 🚀 Installation

```bash
git clone https://github.com/Network-pirate/CC-KILLER.git
cd CC-KILLER
chmod +x launcher.sh
bash launcher.sh
```

> 💡 Ensure Python 3 and required modules are installed.

---

## ⚙️ Setup Instructions

Before running the tool, make sure to:

1. Open each module script under the `module/` folder  
2. Add your **live or test API keys** in the respective fields
   - For example, in `STRIPE_KILLER.py`, replace the API key placeholder:
     ```python
     headers = {
         "Authorization": "Bearer YOUR_STRIPE_SECRET_KEY",
         ...
     }
     ```

3. Save the file

Repeat this for all gateway modules you plan to use.

---

## 💡 How It Works

Each killer script performs:

- Multiple fake charge attempts with **random CVV, expiry, ZIP**
- A final **real charge attempt** with real details
- If the card is declined, it is flagged as **killed**
- If still alive, the process repeats in background

---

## 📦 Supported Gateways

- ✅ Stripe
- ✅ PayPal
- ✅ Square
- ✅ Braintree
- ✅ Authorize.Net
- ✅ SSLCommerz

Each uses its own real-world API structure with fake and final logic, prebuilt by Tawhed.

---

## 🧪 Example Output

```bash
[+] Fake Attempt 1 - Declined ✅
[+] Fake Attempt 2 - Declined ✅
[+] Final Attempt - Declined ✅
[✔] Card successfully killed!
```

---

## 📜 Disclaimer

This tool is intended strictly for:
- Educational research
- Red team simulation
- Ethical testing in controlled environments

❗ **Never use this tool on unauthorized systems or real cards without consent.**  
❗ The developer is **not responsible** for any misuse.

---

## 👤 Author

- GitHub: [Network-pirate](https://github.com/Network-pirate)
- Tool: CC-KILLER
- Coder: **Tawhed**

---

## ❤️ Made with love in Termux & Kali Linux
