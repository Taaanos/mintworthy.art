from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from random import randint
from glitch_this import ImageGlitcher
import utils
import os
import uuid

glitcher = ImageGlitcher()

assets_dir = "assets/"
extension = ".png"

def construct_path(layer):
    path, dirs, files = next(os.walk(assets_dir+ "L" + str(layer)))
    file_count = len(files)
    print(file_count)
    generated_path = assets_dir + "L" + str(layer) + "/" + "l" + str(layer) + "b"+ str(randint(1, file_count)) + extension
    print(generated_path)
    return generated_path

# make_opaque takes an image and makes it opaque by the given factor
# e.g to make an image 20% opaque apply a factor of 0.2
def make_opaque(on_image, factor):
    return texture.putalpha(int(256 * factor))

# resize an image by a factor
# e.g to make it 40% of the orinal apply a factor of 0.4
def scale_image(on_image, factor):
    new_size=(int(on_image.size[0]*factor), int(on_image.size[1]*factor))
    return on_image.resize(new_size)

# rnd_coordinates returns random coordinates based on the randint func
def rnd_coordinates():
    # edge factor regulates how close the layer is applied to the border
    edge_factor = 0.8
    x = randint(0, int(base.size[0]*edge_factor))
    y = randint(0, int(base.size[1]*edge_factor))
    return [x,y];

def draw_words(str_to_draw, layer, size, x, y):
    draw=ImageDraw.Draw(layer)
    font=ImageFont.truetype("Chango-Regular.ttf", size)
    draw.text((x, y), str_to_draw, (256, 256, 256), font=font)

# place_coord creates the coordinates needed to place an in image on the desired position
# needs some experimentation. See examples below.
# x,y  grow from up to bottom
# if you want to place an item on the bottom right corner
# the percentages would be ~ 0.70, 0.90
def place_coord(on_layer,x_perc,y_perc):
    x = int(on_layer.size[0]*x_perc)
    y = int(on_layer.size[1]*y_perc)
    return [x,y];

base=Image.open(construct_path(1))
l2=Image.open(construct_path(2))
l3=Image.open(construct_path(3))
l4=Image.open(construct_path(4))
l5=Image.open(construct_path(5))
logo = Image.open("assets/logo.png")

# Create image to be used as layer0 to create the borders in the final result
border = Image.new('RGB', (int(base.size[0]*1.1), int(base.size[1]*1.1)), color = 'white')

base.paste(l2, (rnd_coordinates()), l2.convert("RGBA"))
base.paste(l5, (rnd_coordinates()), l5.convert("RGBA"))



# base.paste(l3, (0,400), l3.convert("RGBA"))
base.paste(l4, (500,200), l4.convert("RGBA"))
# l1.paste(texture, (x, y), texture)

x,y = place_coord(base,0.3,0.8)
draw_words(".splush", base, 256, x,y)

base=glitcher.glitch_image(base, 2, color_offset=True)

border.paste(base, (int(border.size[0]*0.045),int(border.size[1]*0.025)), base.convert("RGBA"))

logo = scale_image(logo,0.4)
border.paste(logo,place_coord(border,0.71,0.93),logo.convert("RGBA"))
border.show()

border.save("generated/"+str(uuid.uuid1())+".png")