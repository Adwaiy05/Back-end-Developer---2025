import argparse
import json
import os

def load_products():
    # using EAFP principle to load products from products.json
    try:
        with open("products.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_products(products):
    # save the list of products to products.json
    with open("products.json", "w") as file:
        json.dump(products, file, indent=4)

# Cart handling functions
def load_cart():
    if os.path.exists("cart.json"):
        with open("cart.json", "r") as file:
            return json.load(file)
    return []

def save_cart(cart):
    with open("cart.json", "w") as file:
        json.dump(cart, file, indent=4)

# Product management functions
def add_product(args):
    # make sure all necessary product info is provided
    if not args.id or not args.name or args.price is None or args.quantity is None:
        print("Error: All the fields regarding products, (--id, --name, --price, --quantity) are needed to continue.")
        return

    products = load_products()

    # check if product with same ID already exists
    for product in products:
        if product["id"] == args.id:
            print(f"Error: A product with the ID {args.id} already exists.")
            return

    # create entry for new product
    new_product = {
        "id": args.id,
        "name": args.name,
        "price": args.price,
        "quantity": args.quantity
    }

    # add it to the products list and save it to products.json
    products.append(new_product)
    save_products(products)
    print(f"Product {args.name} added with ID {args.id}, price {args.price}, and quantity {args.quantity}.")

def view_products():
    products = load_products()

    if not products:
        print("No products found.")
    else:
        print("Product List:")
        for product in products:
            print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}, Quantity: {product['quantity']}")

def update_product(args):
    if not args.id:
        print("Error: Product ID which needs to be updated is not provided.")
        return

    products = load_products()
    found = False

    # search for product to update
    for product in products:
        if product["id"] == args.id:
            # update only if new values are given
            if args.name:
                product["name"] = args.name
            if args.price is not None:
                product["price"] = args.price
            if args.quantity is not None:
                product["quantity"] = args.quantity
            found = True
            break

    if found:
        save_products(products)
        print(f"Product with ID {args.id} has been updated.")
    else:
        print(f"Error: Product with ID {args.id} was not found.")

def remove_product(args):
    if not args.id:
        print("Error: Product ID which needs to be removed is not provided.")
        return

    products = load_products()
    updated_products = []  # new list to store products that are not removed
    found = False

    # remove the product with the matching ID
    for product in products:
        if product["id"] == args.id:
            found = True
            continue
        updated_products.append(product)

    if found:
        save_products(updated_products)
        print(f"Product with ID {args.id} has been removed.")
    else:
        print(f"Error: Product with ID {args.id} was not found.")

def create_cart():
    save_cart([])  # new cart = empty list
    print("New cart created.")

def add_item(args):
    if not args.id:
        print("Error: In order to add to cart, the Product ID is needed.")
        return
    if args.quantity is None:
        print("Error: In order to add to cart, required quantity is needed.")
        return

    products = load_products()
    product = None

    # find the product by ID
    for p in products:
        if p["id"] == args.id:
            product = p
            break

    if not product:
        print(f"Error: Product ID {args.id} was not found.")
        return

    # check for stock availability compared to required quantity
    if args.quantity > product["quantity"]:
        print(f"Error: Not enough stock for Product ID {args.id}. Available: {product['quantity']}.")
        return

    cart = load_cart()
    item_found = False

    # update quantity if item already in cart
    for item in cart:
        if item["id"] == args.id:
            item["quantity"] += args.quantity
            item_found = True
            break

    # if item not in cart, make a new entry
    if not item_found:
        cart.append({
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": args.quantity
        })

    save_cart(cart)
    print(f"Added {args.quantity} of {product['name']} to the cart.")

def remove_item(args):
    if not args.id:
        print("Error: Product ID is mandatory to remove an item.")
        return

    cart = load_cart()
    updated_cart = []
    item_removed = False

    # remove the item with the given ID
    for item in cart:
        if item["id"] == args.id:
            item_removed = True
            continue
        updated_cart.append(item)

    if item_removed:
        save_cart(updated_cart)
        print(f"Product with ID {args.id} has been removed from the cart.")
    else:
        print(f"Error: Product with ID {args.id} was not found in the cart.")

def view_cart():
    cart = load_cart()

    if not cart:
        print("Cart is empty.")
        return
    
    print("Current Cart:")
    total = 0.0
    validation_errors = [] # a list to collect validation errors

    # go through each item in cart and print its details
    for item in cart:
        quantity = item["quantity"]
        name = item["name"]
        price = item["price"]
        # check if quantity is a valid positive integer and if not, add to validation errors list
        if not isinstance(quantity, int) or quantity <= 0:
            validation_errors.append(f"Invalid quantity of '{name}' : 'quantity' must be a positive integer.")
        # check if price is a valid number and if not, add to validation errors list
        if not isinstance(price, (int,float)) or price < 0:
            validation_errors.append(f"Invalid price of '{name}' : 'price' must be a non-negative float/integer.")
        # if there are no validation items, continue with calculation
        if not validation_errors:
            print(f"{quantity} x {name} @ {price} each")
            total = total + (price * quantity)

    # if validation errors are found, raise an error and compile all errors into one message
    if validation_errors:
        raise ValueError("Validation Errors:\n" + "\n".join(validation_errors))
    
    print(f"Total: {round(total, 2)}")
    return total 

def checkout():
    cart = load_cart()

    if not cart:
        print("Error: Cart is empty.")
        return

    products = load_products()
    total = 0.0

    # subtract items from stock after checkout and calculate total
    for item in cart:
        for product in products:
            if product["id"] == item["id"]:
                product["quantity"] = product["quantity"] - item["quantity"]
                break
        total = total + (item["price"] * item["quantity"])

    save_products(products)
    save_cart([])  # empty cart to act like a new cart after checkout

    print(f"Checkout complete. Total amount due: {round(total, 2)}.")
    print("Receipt:")
    for item in cart:
        print(f"{item['quantity']} x {item['name']} @ {item['price']} each")
    print(f"Total: {round(total, 2)}")

def print_stock():
    products = load_products()

    if not products:
        print("No stock available.")
    else:
        print("Stock List:")
        for product in products:
            print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}, Quantity: {product['quantity']}")

def main(argv=None):
    parser = argparse.ArgumentParser(description="Stock Manager CLI")

    # define all the possible actions to be performed
    parser.add_argument('--add_product', action='store_true')
    parser.add_argument('--view_products', action='store_true')
    parser.add_argument('--update_product', action='store_true')
    parser.add_argument('--remove_product', action='store_true')
    parser.add_argument('--create_cart', action='store_true')
    parser.add_argument('--add_item', action='store_true')
    parser.add_argument('--remove_item', action='store_true')
    parser.add_argument('--view_cart', action='store_true')
    parser.add_argument('--checkout', action='store_true')
    parser.add_argument('--print_stock', action='store_true')

    # arguments that the actions might require
    parser.add_argument('--id')
    parser.add_argument('--name')
    parser.add_argument('--price', type=float)
    parser.add_argument('--quantity', type=int)

    args = parser.parse_args(argv)

    # call the correct function based on the command
    if args.add_product:
        add_product(args)
    elif args.view_products:
        view_products()
    elif args.update_product:
        update_product(args)
    elif args.remove_product:
        remove_product(args)
    elif args.create_cart:
        create_cart()
    elif args.add_item:
        add_item(args)
    elif args.remove_item:
        remove_item(args)
    elif args.view_cart:
        view_cart()
    elif args.checkout:
        checkout()
    elif args.print_stock:
        print_stock()

if __name__ == "__main__":
    main()
