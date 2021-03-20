from PIL import Image
from random import randint

background = Image.open("assets/background.jpg")
dogo = Image.open("assets/dogo.png")

newsize = (900,1600)
background = background.resize(newsize)

# background.paste(dogo, (1500,1500), dogo.convert('RGBA'))
x = randint(0, background.size[0])
y = randint(0, background.size[1])

# paste dogo in random coordinates in background image
background.paste(dogo, (x,y), dogo.convert('RGBA'))
background.show()