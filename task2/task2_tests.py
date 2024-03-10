import unittest
from task2 import create_image_from_text
from task2 import character_to_color

class TestImageCreation(unittest.TestCase):
    
    def test_characters(self):
        file_path = "Test_data/sample.txt"
        image = create_image_from_text(file_path)
        pixels = image.load()
        with open(file_path, 'r') as file:
            lines = [line.strip('\n') for line in file.readlines()]
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                self.assertTrue(
                    pixels[x, y] == character_to_color[char],
                    f"The pixel at position ({x}, {y}) have different color: \
                    got {pixels[x, y]}, expected {character_to_color[char]}"
                )
    
    def test_error_characters(self):
        file_path = "Test_data/test_matrix.txt"
        try:
            create_image_from_text(file_path)
            raise AssertionError("The program exit succesfully!")
        except ValueError as err:
            error_x_ind = "1"
            error_y_ind = "2"
            error_msg = str(err)
            self.assertTrue(
                error_msg.find(error_x_ind) != -1 and error_msg.find(error_y_ind) != -1,
                f"The error file does not contain info about problem indices!"
            )
    
if __name__ == '__main__':
    unittest.main()