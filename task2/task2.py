from PIL import Image

# Assign colors to each symbol and draw it on the image
character_to_color = {
    "S": (128, 128, 128),
    "R": (0, 0, 0),
    "C": (255, 0, 0),
    "G": (0, 255, 0),
    "B": (200, 200, 200),
    "P": (50, 50, 50),
    "T": (253, 102, 0),
    # This is for space character, the "unknown" pixel
    " ": (255, 255, 255)
}

def create_image_from_text(file_path, output_path):
    # Open the text file and read its contents without \n symbols
    with open(file_path, 'r') as file:
        lines = [line.strip('\n') for line in file.readlines()]

    # Determine the dimensions of the matrix
    num_lines = len(lines)
    max_line_length = max(len(line) for line in lines)

    # Create a blank white image to draw on
    image = Image.new('RGB', (max_line_length, num_lines), color = 'white')
    pixels = image.load()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char not in character_to_color:
                raise ValueError(
                    f"The character {char} at the position ({x}, {y}) is not on the list of allowed characters!\n" \
                    "Please refer to the ASSIGNMENT.md for the list of allowed characters."
                )
            color_value = ord(char)
            pixels[x, y] = character_to_color[char]

    # Save the image
    image.save(output_path)

if __name__ == "__main__":
    print("This program designed for converting a text matrix into image. For more details please referer to ASSIGNMENT.md")
    input_file = input("Enter the path to the text file: ")
    output_file = input("Enter the path for the output image: ")

    try:
        create_image_from_text(input_file, output_file)
        print("Image created successfully!")
    except ValueError as err:
        print("Image not created due to value error")
        print(err)
    except Exception as err:
        print("Image not created due to unexpected error")
        print(f"{err=}, {type(err)=}")