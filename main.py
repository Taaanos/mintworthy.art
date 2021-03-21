from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from random import randint
from glitch_this import ImageGlitcher
import utils
import os
import uuid
from web3.auto.infura import w3

glitcher = ImageGlitcher()

assets_dir = "assets/"
extension = ".png"


# construct_path constructs the path for the assets.
# Reads the number of files on the given layer
# and uses one with equal probability
def construct_path(layer):
    path, dirs, files = next(os.walk(assets_dir + "L" + str(layer)))
    file_count = len(files)
    generated_path = assets_dir + "L" + str(layer) + "/" + "l" + str(
        layer) + "b" + str(randint(1, file_count)) + extension
    return generated_path


# make_opaque takes an image and makes it opaque by the given factor
# e.g to make an image 20% opaque apply a factor of 0.2
def make_opaque(on_image, factor):
    return texture.putalpha(int(256 * factor))


# resize an image by a factor
# e.g to make it 40% of the orinal apply a factor of 0.4
def scale_image(on_image, factor):
    new_size = (int(on_image.size[0] * factor), int(on_image.size[1] * factor))
    return on_image.resize(new_size)


# rnd_coordinates returns random coordinates based on the randint func
def rnd_coordinates():
    # edge factor regulates how close the layer is applied to the border
    edge_factor = 0.8
    x = randint(0, int(bg.size[0] * edge_factor))
    y = randint(0, int(bg.size[1] * edge_factor))
    return [x, y]


# draw_words writes a word given the string to write,
# the layer to write it on, the size of the font and
# the coordinates
def draw_words(str_to_draw, layer, size, color, x, y):
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype("FredokaOne-Regular.ttf", size)
    draw.text((x, y), str_to_draw, "#" + color, font=font)


# draw_multiline draws a string and respects the newlines
def draw_multiline(str_to_draw, layer, size, x, y):
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype("FredokaOne-Regular.ttf", size)
    draw.multiline_text((x, y),
                        str_to_draw,
                        font=font,
                        fill=(256, 256, 256),
                        spacing=100)


# draw_circle draws a circle on the given layer
def draw_circle(layer, x, y):
    draw = ImageDraw.Draw(layer)
    circle_radius_factor = 0.6
    draw.pieslice([(x, y),
                   (x + layer.size[0] * circle_radius_factor,
                    y + layer.size[0] * circle_radius_factor)],
                  0,
                  360,
                  fill='#' + colors[randint(0,
                                            len(colors) - 1)])


# place_coord creates the coordinates needed to
# place an in image on the desired position
# needs some experimentation. See examples below.
# x,y  grow from up to bottom
# if you want to place an item on the bottom right corner
# the percentages would be ~ 0.70, 0.90
def place_coord(on_layer, x_perc, y_perc):
    x = int(on_layer.size[0] * x_perc)
    y = int(on_layer.size[1] * y_perc)
    return [x, y]


# get latest block hash as string
# connected to infura
def get_block_hash():
    block = w3.eth.get_block('latest')
    hash = block.hash.hex()
    print("generated on ⏱ : " + hash)
    return hash


bg = Image.open(construct_path(1))
insect = Image.open(construct_path(2))
plant = Image.open(construct_path(5))
signature = Image.open("assets/signature.png")
logo = Image.open("assets/logo.png")

# Create image to be used as layer0 to become the borders of the final canvas
border = Image.new('RGB', (int(bg.size[0] * 1.1), int(bg.size[1] * 1.1)),
                   color='white')

colors = [
    'a1cae2', 'c2b092', 'cfc5a5', 'eae3c8', 'ffaec0', 'ffd384', 'ffab73',
    'e4bad4', 'f6dfeb', 'caf7e3'
]
colored_blank_image = Image.new('RGB', (int(bg.size[0]), int(bg.size[1])),
                                color='#' + colors[randint(0,
                                                           len(colors) - 1)])
bg = colored_blank_image

x_circle, y_circle = place_coord(bg, 0.2, 0.2)
draw_circle(bg, x_circle, y_circle)
bg.paste(insect, (rnd_coordinates()), insect.convert("RGBA"))
insect = Image.open(construct_path(2))
bg.paste(insect, (rnd_coordinates()), insect.convert("RGBA"))
bg = glitcher.glitch_image(bg, 8, color_offset=True)
bg.paste(plant, (rnd_coordinates()), plant.convert("RGBA"))

# draw .word
words = [
    '.visualise', '.imagine', '.think', '.empower', '.explore', '.engage',
    '.motivate', '.inspire', '.aspire', '.belong', '.accept', '.defy',
    '.exist', '.transcend', '.catalyse', '.overcome', '.dismantle',
    '.meditate', '.reflect', '.express'
]
x, y = place_coord(bg, 0.05, 0.9)
draw_words(words[randint(0, len(words) - 1)], bg, 256, "ffffff", x, y)

# draw one letter
letters = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]
x_letter, y_letter = place_coord(bg, 0.75, 0.02)
draw_words(letters[randint(0,
                           len(letters) - 1)], bg, 512, "ffffff", x_letter,
           y_letter)

#draw number next to letter
draw_words(str(randint(0, 100)), bg, 96, "ffffff", x_letter * 1.2,
           y_letter * 1.5)

# draw multiline text
x, y = place_coord(bg, 0.2, 0.4)
phrases = [
    'What\ninspires\nyou?', 'What\ninspires\nyou?',
    'Am I\nusing my\ntime wisely?', 'Am I taking \nanything for\ngranted?',
    'Am I employing\na healthy perspective?', 'Am I living\ntrue to myself?',
    'Am I waking up\nin the morning ready\nto take on the day?',
    'Am I taking\ncare of myself\nphysically?',
    'Am I achieving\nthe goals that I have\nset for myself?',
    'Who am I, really?'
]

x, y = place_coord(bg, 0.1, 0.1)
draw_multiline(phrases[randint(0, len(phrases) - 1)], bg, 128, x, y_letter * 2)

border.paste(bg, (int(border.size[0] * 0.045), int(border.size[1] * 0.035)),
             bg.convert("RGBA"))

signature = scale_image(signature, 0.4)
logo = scale_image(logo, 0.15)
border.paste(signature, place_coord(border, 0.71, 0.93),
             signature.convert("RGBA"))
border.paste(logo, place_coord(border, 0.68, 0.943), logo.convert("RGBA"))

# draw hash
x, y = place_coord(border, 0.045, 0.96)
draw_words(get_block_hash(), border, 32, "bbbbbb", x, y)
# border.show()

# reduce the generated image size. Reduce is not compress.
# Reduce touches the resolution.
# border = border.reduce(3)
border.save("generated/" + str(uuid.uuid1()) + ".png")
