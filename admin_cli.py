import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def show_menu():
    print("\n--- Admin Inventory Portal ---")
    print("1. View Inventory")
    print("2. Add Item")
    print("3. Fetch External Product (Barcode)")
    print("4. Exit")

def run_cli():
    while True:
        show_menu()
        choice = input("Select an option: ")
        
        if choice == '1':
            res = requests.get(f"{BASE_URL}/inventory")
            print(res.json())
        elif choice == '2':
            name = input("Item Name: ")
            qty = int(input("Quantity: "))
            requests.post(f"{BASE_URL}/inventory", json={"name": name, "quantity": qty})
            print("Item added.")
        elif choice == '3':
            bc = input("Enter Barcode: ")
            res = requests.get(f"{BASE_URL}/fetch-product/{bc}")
            print(res.json())
        elif choice == '4':
            sys.exit()

if __name__ == "__main__":
    run_cli()
