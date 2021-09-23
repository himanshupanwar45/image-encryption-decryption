from PIL import Image
from random import randint
import numpy
import sys
import helperModule


im = Image.open('input\pic1.png')
pix = im.load()

print(pix[0, 1])
