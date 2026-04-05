import requests

BASE_URL = "http://127.0.0.1:5000"

def menu():
    print("\nInventory CLI")
    print("1. View items")
    print("2. Add item")
    print("3. Update item")
    print("4. Delete item")
    print("5. Search product (API)")
    print("6. Exit")

def view_items():
    res = requests.get(f"{BASE_URL}/inventory")
    print(res.json())

def add_item():
    name = input("Name: ")
    quantity = int(input("Quantity: "))
    price = float(input("Price: "))
    barcode = input("Barcode: ")

    data = {
        "name": name,
        "quantity": quantity,
        "price": price,
        "barcode": barcode
    }

    res = requests.post(f"{BASE_URL}/inventory", json=data)
    print(res.json())

def update_item():
    item_id = input("Item ID: ")
    price = float(input("New Price: "))

    res = requests.patch(f"{BASE_URL}/inventory/{item_id}", json={"price": price})
    print(res.json())

def delete_item():
    item_id = input("Item ID: ")
    res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    print(res.json())

def search_api():
    barcode = input("Enter barcode: ")
    res = requests.get(f"{BASE_URL}/external/product?barcode={barcode}")
    print(res.json())

def main():
    while True:
        menu()
        choice = input("Choose: ")

        if choice == "1":
            view_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            search_api()
        elif choice == "6":
            break

if __name__ == "__main__":
    main()