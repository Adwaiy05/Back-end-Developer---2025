import unittest
from stock_manager import save_products, save_cart, view_cart

class TestCartTotal(unittest.TestCase):
    def test_total_with_wrong_product_details_in_cart(self):
        bad_product = {
            "id": "259",
            "name": "Dishwasing Liquid",
            "price": "price",  
            "quantity": -2      
        }

        save_products([bad_product])
        save_cart([bad_product])

        with self.assertRaises(ValueError) as context:
            view_cart()

        error_message = str(context.exception)
        self.assertIn("Invalid quantity of", error_message)
        self.assertIn("Invalid price of", error_message)
        print(f"{error_message}")

if __name__ == '__main__':
    unittest.main()