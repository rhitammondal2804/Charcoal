"""
CHARCOAL  -  Sketch your world in characters.
A photo-to-ASCII art studio for your Code in Place final project.

HOW TO RUN  (this runs on your own computer in PyCharm -- NOT inside
the Code in Place web IDE; see the note at the very bottom for why):
  1. Install the imaging library once:   pip install Pillow
  2. Put this file and your photo in the SAME folder.
  3. Run the file, type your photo's filename, and pick a style.

CONCEPTS USED
  Reading image pixels, nested loops, functions, dictionaries,
  strings, conditionals, user input, and a little brightness math.
"""

from PIL import Image


# Each style is a "ramp" of characters ordered from DARKEST to LIGHTEST.
# Dark parts of the photo use the dense characters on the left, and
# bright parts use the spaced-out characters on the right. This reads
# correctly on a normal light background; use the invert option below
# if your output sits on a dark background.
STYLES = {
    "1": ("Classic Shade", "@%#*+=-:. "),
    "2": ("Solid Blocks", "\u2588\u2593\u2592\u2591 "),
    "3": ("Soft Sketch", "#?x+:-. "),
}

DEFAULT_WIDTH = 80


def get_brightness(red, green, blue):
    """Return how bright a pixel looks, from 0 (black) to 255 (white)."""
    # Weighted to match how the human eye perceives each color.
    return 0.299 * red + 0.587 * green + 0.114 * blue


def pixel_to_char(brightness, ramp):
    """Map a 0-255 brightness value to a single character in the ramp."""
    index = int(brightness / 256 * len(ramp))
    if index >= len(ramp):
        index = len(ramp) - 1
    return ramp[index]


def make_ascii_art(image, ramp, output_width):
    """Build and return the whole ASCII picture as one big string."""
    width, height = image.size
    # How many real pixels we skip per character, left to right.
    step = max(1, width // output_width)
    # Characters are about twice as tall as they are wide, so we skip
    # twice as many rows to keep the picture from looking stretched.
    row_step = step * 2

    art = ""
    for y in range(0, height, row_step):
        line = ""
        for x in range(0, width, step):
            red, green, blue = image.getpixel((x, y))
            brightness = get_brightness(red, green, blue)
            line += pixel_to_char(brightness, ramp)
        art += line + "\n"
    return art


def ask_for_width():
    """Ask how wide the art should be, with a safe default."""
    answer = input("How wide should the art be? (40-120, Enter for 80): ")
    if answer.strip() == "":
        return DEFAULT_WIDTH
    try:
        width = int(answer)
    except ValueError:
        return DEFAULT_WIDTH
    if width < 20:
        width = 20
    if width > 200:
        width = 200
    return width


def print_banner():
    print("=" * 46)
    print("            C H A R C O A L")
    print("     Sketch your world in characters")
    print("=" * 46)


def main():
    print_banner()

    filename = input("Enter your image filename (e.g. selfie.jpg): ")

    # Load the image, and fail gracefully if the name is wrong.
    try:
        image = Image.open(filename).convert("RGB")
    except Exception:
        print("Hmm, I couldn't open '" + filename + "'.")
        print("Make sure the photo is in the same folder, then try again.")
        return

    print("")
    print("Choose a style:")
    for key in STYLES:
        print("  " + key + ") " + STYLES[key][0])
    choice = input("Your choice (1-3): ")
    if choice not in STYLES:
        choice = "1"
    style_name, ramp = STYLES[choice]

    output_width = ask_for_width()

    answer = input("Viewing on a dark background? Invert it. (y/n): ")
    if answer.lower().startswith("y"):
        ramp = ramp[::-1]

    print("")
    print("Drawing your portrait in '" + style_name + "' ...")
    print("")
    art = make_ascii_art(image, ramp, output_width)
    print(art)

    # Offer to save the result alongside the program.
    save = input("Save this to 'charcoal_art.txt'? (y/n): ")
    if save.lower().startswith("y"):
        try:
            out_file = open("charcoal_art.txt", "w", encoding="utf-8")
            out_file.write(art)
            out_file.close()
            print("Saved! Open 'charcoal_art.txt' to see your masterpiece.")
        except Exception:
            print("Couldn't save a file here, but your art is right above.")

    print("")
    print("Thanks for using Charcoal. Go make something beautiful.")


if __name__ == "__main__":
    main()
