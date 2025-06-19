import unittest
import os
from sort_file import main

class TestMyCLP(unittest.TestCase):
    def test_int_sort(self):
        # We open an input file in write mode (w) and then write our test data in it
        with open("input.txt", "w") as f:
            f.write("2\n1\n3\n")
        # Running our main() function from the sorter code with the required arguments 
        main(["-o", "output.txt", "input.txt"])
        # We open the output file in read mode (r) and then copy the contents into a variable called actual_result
        with open("output.txt", "r") as f:
            actual_result = f.read()
        # We use the assertEqual tool to compare that our actual results (actual_result) match our expected results (1\n2\n3\n)
        self.assertEqual(actual_result, "1\n2\n3\n")

        os.remove("input.txt")
        os.remove("output.txt")

    def test_int_sort_rev(self):
        with open("input.txt", "w") as f:
            f.write("2\n1\n3\n")

        main(["-r", "-o", "output.txt", "input.txt"])

        with open("output.txt", "r") as f:
            actual_result = f.read()

        self.assertEqual(actual_result, "3\n2\n1\n")

        os.remove("input.txt")
        os.remove("output.txt")

    def test_string_sort(self):
        with open("input.txt", "w") as f:
            f.write("mango\napple\nblueberry\n")

        main(["-o", "output.txt", "input.txt"])

        with open("output.txt", "r") as f:
            actual_result = f.read()

        self.assertEqual(actual_result, "apple\nblueberry\nmango\n")

        os.remove("input.txt")
        os.remove("output.txt")

    def test_string_sort_rev(self):
        with open("input.txt", "w") as f:
            f.write("mango\napple\nblueberry\n")

        main(["-r", "-o", "output.txt", "input.txt"])

        with open("output.txt", "r") as f:
            actual_result = f.read()

        self.assertEqual(actual_result, "mango\nblueberry\napple\n")

        os.remove("input.txt")
        os.remove("output.txt")
        
if __name__ == "__main__":
    unittest.main()
