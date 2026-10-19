# cli.py - the text menu (the "user interface")
# 1) Start the server first:  python app.py
# 2) Then run this file in a second terminal:  python cli.py
import requests

URL = "http://127.0.0.1:5000"


def print_item(item):
    product = item["product"]
    print(item["id"], "|", product["product_name"], "|", product["brands"],
          "| $" + str(item["price"]), "| stock:", item["stock"])


def view_all():
    response = requests.get(URL + "/inventory")
    for item in response.json():
        print_item(item)


def view_one():
    item_id = input("Item id: ")
    response = requests.get(URL + "/inventory/" + item_id)
    if response.status_code == 200:
        print_item(response.json())
    else:
        print("Error:", response.json()["error"])


def add_item():
    data = {
        "product_name": input("Name: "),
        "brands": input("Brand: "),
        "price": input("Price: "),
        "stock": input("Stock: "),
    }
    response = requests.post(URL + "/inventory", json=data)
    if response.status_code == 201:
        print("Item added!")
    else:
        print("Error:", response.json()["error"])


def update_item():
    item_id = input("Item id: ")
    data = {}
    price = input("New price (Enter to skip): ")
    stock = input("New stock (Enter to skip): ")
    if price != "":
        data["price"] = price
    if stock != "":
        data["stock"] = stock
    response = requests.patch(URL + "/inventory/" + item_id, json=data)
    if response.status_code == 200:
        print("Item updated!")
    else:
        print("Error:", response.json()["error"])


def delete_item():
    item_id = input("Item id: ")
    response = requests.delete(URL + "/inventory/" + item_id)
    if response.status_code == 200:
        print("Item deleted!")
    else:
        print("Error:", response.json()["error"])


def find_on_api():
    choice = input("Search by 1) barcode or 2) name? ")
    if choice == "1":
        search = {"barcode": input("Barcode: ")}
    elif choice == "2":
        search = {"name": input("Name: ")}
    else:
        print("Please type 1 or 2.")
        return

    response = requests.get(URL + "/lookup", params=search)
    if response.status_code != 200:
        print("Error:", response.json()["error"])
        return

    product = response.json()["product"]
    print("Found:", product.get("product_name"), "|", product.get("brands"))

    answer = input("Add to inventory? (y/n) ")
    if answer == "y":
        search["price"] = input("Price: ")
        search["stock"] = input("Stock: ")
        response = requests.post(URL + "/inventory/from-api", json=search)
        if response.status_code == 201:
            print("Item added!")
        else:
            print("Error:", response.json()["error"])


def main():
    while True:
        print("\n1. Check all items")
        print("2. Check one item")
        print("3. Add item")
        print("4. Update price or stock")
        print("5. Delete item")
        print("6. Find item on OpenFoodFacts")
        print("0. Quit")
        choice = input("Choose: ")

        # try/except catches problems like "server is not running"
        try:
            if choice == "1":
                view_all()
            elif choice == "2":
                view_one()
            elif choice == "3":
                add_item()
            elif choice == "4":
                update_item()
            elif choice == "5":
                delete_item()
            elif choice == "6":
                find_on_api()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Please try agin choosing a no.")
        except requests.exceptions.RequestException:
            print("Error: could not reach the API. Is app.py running?")


if __name__ == "__main__":
    main()