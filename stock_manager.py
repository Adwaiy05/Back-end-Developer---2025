import argparse
import json
import os

# Product handling functions
def load_products():
    # checks if a file called products.json exists. If yes, the contents of the file are stored in a variable called products. However, if no, an empty list is returned
    if os.path.exists("products.json"):
        with open("products.json", "r") as file:
            return json.load(file)
    return [] # [] = empty list

def save_products(products):
    # saves products list to a file called products.json in JSON format with indents to look more organized 
    with open("products.json", "w") as file:
        json.dump(products, file, indent=4)

# Cart handling functions 
def load_cart():
    # checks if a file called cart.json exists. If yes, the contents of the file are stored in a variable called cart. However, if no, an empty list is returned
    if os.path.exists("cart.json"):
        with open("cart.json", "r") as file:
            return json.load(file)
    return [] # [] = empty list

def save_cart(cart):
    # saves list from cart to a file called cart.json in JSON format with indents to look more organized 
    with open("cart.json", "w") as file:
        json.dump(cart, file, indent=4)

# main()
def main(argv=None): # argv=None allows for unit testing by passing arguments manually
    parser = argparse.ArgumentParser(description="Stock Manager CLI")

    # Command flags. "action" is used to specify which action to perform
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

    # Product/cart arguments
    parser.add_argument('--id')
    parser.add_argument('--name')
    parser.add_argument('--price', type=float)
    parser.add_argument('--quantity', type=int)

    # Parse arguments
    args = parser.parse_args(argv)

    # Add Product block
    if args.add_product:
        # check if the essential fields have been provided by the user. [Price and quantity can hold 0 as a valid value BUT we want to check if they are empty, so we use (None)]
        if not args.id or not args.name or args.price is None or args.quantity is None:
            print("Error: All the fields regarding products, (--id, --name, --price, --quantity) are needed to continue.")
            # stop any further execution
            return
        # load existing list from products.json into variable called products  
        products = load_products()
        # loop through each item in our products list and check if existing product ID matches with the one provided by the user
        for product in products:
            if product["id"] == args.id:
                print(f"Error: A product with the ID {args.id} already exists.")
                return
        # if no product with identical ID is found, create a new product dictionary 
        new_product = {
            "id": args.id,
            "name": args.name,
            "price": args.price,
            "quantity": args.quantity
        }
        # Add new product to the end of the existing list and then save permanently to products.json
        products.append(new_product)
        save_products(products)
        print(f"Product {args.name} added with ID {args.id}, price {args.price}, and quantity {args.quantity}.")

    # View Products block
    elif args.view_products:
        # load existing products from products.json to a variable called products
        products = load_products()
        # check if products list is empty
        if not products:
            print("No products found.")
        else:
            print("Product List:")
            # loop through each product in products list and print the details
            for product in products:
                print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}, Quantity: {product['quantity']}")

    # Update Product block
    elif args.update_product:
        # check for essential fields
        if not args.id:
            print("Error: Product ID which needs to be updated is not provided.")
            # stop any further execution
            return

        products = load_products()
        # check if product with provided ID even exists
        found = False
        for product in products:
            if product["id"] == args.id:
                # if found to exist, update fields based on user input
                if args.name:
                    product["name"] = args.name
                if args.price is not None:
                    product["price"] = args.price
                if args.quantity is not None:
                    product["quantity"] = args.quantity
                found = True
                break
        # save the updated products list back to products.json ONLY if product with exact ID provided was found
        if found:
            save_products(products)
            print(f"Product with ID {args.id} has been updated.")
        else:
            print(f"Error: Product with ID {args.id} was not found.")

    # Remove Product block
    elif args.remove_product:
        # check for essential fields
        if not args.id:
            print("Error: Product ID which needs to be removed is not provided.")
            return

        products = load_products()
        # loop through all products in products list, one by one, and remove the one with matching ID
        updated_products = [] # new list to hold remaining products but starts with an empty list 
        found = False

        for product in products:
            if product["id"] == args.id:
                found = True
                continue
            # add all products which don't match the ID provided to the new list
            updated_products.append(product)
        # ONLY if product with provided ID was found, save the new, updated list back to products.json (without the product with the matching ID)
        if found:
            save_products(updated_products)
            print(f"Product with ID {args.id} has been removed.")
        else:
            print(f"Error: Product with ID {args.id} was not found.")

    # Create Cart block
    elif args.create_cart:
        save_cart([])  # empty list = new cart
        print("New cart created.")

    # Add Items to Cart block
    elif args.add_item:
        # check for essential fields
        if not args.id:
            print("Error: In order to add to cart, the Product ID is needed.")
            return
        if args.quantity is None:
            print("Error: In order to add to cart, required quantity is needed.")
            return

        products = load_products()
        # check all products in products list to find the one with the matching ID
        product = None
        for p in products:
            if p["id"] == args.id:
                product = p
                break

        if not product:
            print(f"Error: Product ID {args.id} was not found.")
            return
        # error handling for when the quantity demanded by user is more than what is available in stock
        if args.quantity > product["quantity"]:
            print(f"Error: Not enough stock for Product ID {args.id}. Available: {product['quantity']}.")
            return
        # load existing cart from cart.json
        cart = load_cart()
        # check if item already exists in cart
        item_found = False
        # loop through eact item in cart
        for item in cart:
            if item["id"] == args.id:
                # if item with matching ID is found, just increase its quantity in the cart
                item["quantity"] += args.quantity
                item_found = True
                # stop loop
                break
        # if item with matching ID not found in cart, make a new entry into the cart
        if not item_found:
            cart.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": args.quantity
            })
        # save updated cart back to cart.json
        save_cart(cart)
        print(f"Added {args.quantity} of {product['name']} to the cart.")

    # Remove Item from Cart block 
    elif args.remove_item:
        # check for essential fields
        if not args.id:
            print("Error: Product ID is mandatory to remove an item.")
            return
        # open cart.json and load existing items in cart to variable called cart
        cart = load_cart()
        # cart after removing an item will be saved here but it starts off as an empty file
        updated_cart = []
        # loop through each item in cart
        item_removed = False
        # if item with matching ID is found, remove it from cart and save rest of the cart to updated_cart
        for item in cart:
            if item["id"] == args.id:
                item_removed = True
                continue
            updated_cart.append(item)
        #save updated cart back to cart.json ONLY if item with matching ID was found AND removed
        if item_removed:
            save_cart(updated_cart)
            print(f"Product with ID {args.id} has been removed from the cart.")
        else:
            print(f"Error: Product with ID {args.id} was not found in the cart.")

    # View Cart block
    elif args.view_cart:
        # load existing items from cart.json to variable called cart
        cart = load_cart()
        # check for empty cart
        if not cart:
            print("Cart is empty.")
        else:
            print("Current Cart:")
            # variable to hold total amount for value of items in cart but starts off at 0.0
            total = 0.0
            # loop through each item in cart and output its necessary details
            for item in cart:
                name = item["name"]
                price = item["price"]
                quantity = item["quantity"]
                print(f"{quantity} x {name} @ {price} each")
                # continue adding to total after each item's (price * quantity) value is known
                total += price * quantity
                # output the final total amount to 2 d.p
            print(f"Total: {round(total, 2)}")

    # Checkout block
    elif args.checkout:
        cart = load_cart()
        # check for empty cart
        if not cart:
            print("Error: Cart is empty.")
            return
        # load existing products from products.json to variable called products
        products = load_products()
        # 
        total = 0.0

        for item in cart:
            for product in products:
                if product["id"] == item["id"]:
                    product["quantity"] -= item["quantity"]
                    break
            total += item["price"] * item["quantity"]
        # sae updated products list back to products.json
        save_products(products)
        save_cart([])  # empty cart to look like new cart after a checkout
        # print statements to match the desired format of output 
        print(f"Checkout complete. Total amount due: {round(total, 2)}.")
        print("Receipt:")
        for item in cart:
            print(f"{item['quantity']} x {item['name']} @ {item['price']} each")
        print(f"Total: {round(total, 2)}")

    # Print Stock block
    elif args.print_stock:
        # load existing products from products.json to variable called products
        products = load_products()
        # check for empty products list. If not empty, print remaining stock along with product details
        if not products:
            print("No stock available.")
        else:
            print("Stock List:")
            for product in products:
                print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}, Quantity: {product['quantity']}")

if __name__ == "__main__":
    main()