import unittest
import os
from sort_file import main

class TestMyCLP(unittest.TestCase):
    def test_sort(self):
        input_file = "input.txt"
        output_file = "output.txt"
        # We open an input file in write mode (w) and then write our test data in it
        with open(input_file, "w") as f:
            f.write("3\n1\n2\n")
        # Running our main() function from the sorter code with the same command:  py sort_file.py -r -o out_file example_file
        main(["-r", "-o", output_file, input_file])
        # We open the output file in read mode (r) and then copy the contents into a variable called actual_result
        with open(output_file, "r") as f:
            actual_result = f.read()
        # We use the assertEqual tool to compare that our actual results (actual_result) match our expected results (3\n2\n1\n)
        self.assertEqual(actual_result, "3\n2\n1\n")

        os.remove(input_file)
        os.remove(output_file)

if __name__ == "__main__":
    unittest.main()