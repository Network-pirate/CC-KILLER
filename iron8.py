import os
import time

def loading_animation(text="Loading", duration=1.5):
    stages = ["[🔲⬜⬜⬜⬜]", "[🔲🔲⬜⬜⬜]", "[🔲🔲🔲⬜⬜]", "[🔲🔲🔲🔲⬜]", "[🔲🔲🔲🔲🔲]"]
    end_time = time.time() + duration
    while time.time() < end_time:
        for stage in stages:
            print(f"\r{text} {stage}", end="", flush=True)
            time.sleep(0.2)
    print("\r" + " " * 30, end="\r")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_script(script_name):
    loading_animation("Launching")
    script_path = os.path.join("module", script_name)
    os.system(f"python3 \"{script_path}\"" if os.name != 'nt' else f"python \"{script_path}\"")

def main():
    while True:
        clear()
        print("\033[95m" + "╔" + "═" * 34 + "╗")
        print("║\033[96m{:^34}\033[95m║".format("TAWHED"))
        print("║\033[92m{:^34}\033[95m║".format("💳 CC Killer Project"))
        print("╚" + "═" * 34 + "╝\033[0m\n")

        print("\033[93mSelect a module to run:\033[0m\n")
        print(" 1. PayPal Killer")
        print(" 2. Stripe Killer")
        print(" 3. Square Killer")
        print(" 4. Authorize Killer")
        print(" 5. Braintree Killer")
        print(" 6. SSLCommerz Killer")
        print(" 7. Exit")

        choice = input("\n\033[94mEnter your choice (1-7): \033[0m")

        mapping = {
            "1": "PAYPAL_KILLER.py",
            "2": "STRIPE_KILLER.py",
            "3": "SQUARE_KILLER.py",
            "4": "AUTHORIZE_KILLER.py",
            "5": "BRAINTREE_KILLER.py",
            "6": "SSLCommerz_KILLER.py"
        }

        if choice in mapping:
            run_script(mapping[choice])
        elif choice == "7":
            print("\n\033[92mGoodbye, TAWHED! 👋\033[0m")
            break
        else:
            print("\n\033[91mInvalid option. Please try again.\033[0m")
            time.sleep(1.5)

if __name__ == "__main__":
    main()
