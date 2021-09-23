from PIL import Image
from random import randint
import numpy
import sys
import helperModule


def encrypt_image(path):
    im = Image.open(path)
    pix = im.load()

    # obtaining the rgb matrix of the image
    r = []
    g = []
    b = []

    for i in range(im.size[0]):
        r.append([])
        g.append([])
        b.append([])
        for j in range(im.size[1]):
            rgbPerPixel = pix[i, j]
            r[i].append(rgbPerPixel[0])
            g[i].append(rgbPerPixel[1])
            b[i].append(rgbPerPixel[2])

    # number of rows in image
    rows = im.size[0]

    # number of columns in image
    columns = im.size[1]

    # value of alpha
    alpha = 8

    # Generation of random vector Kr
    Kr = [randint(0, pow(2, alpha - 1)) for i in range(rows)]
    # Generation of random vector Kc
    Kc = [randint(0, pow(2, alpha - 1)) for i in range(columns)]

    fKr = open('keys/Kr.txt', 'w+')
    fKc = open('keys/Kc.txt', 'w+')
    fIter = open('keys/ITER.txt', 'w+')

    # writing value of Kr in file
    for i in Kr:
        fKr.write(str(i) + '\n')

    # writing value of Kc in file
    for i in Kc:
        fKc.write(str(i) + '\n')

    # number of iterations
    ITER = 1
    # f.write(' Value of max iterations : ')
    fIter.write(str(ITER))

    # algorithm begins
    for iterations in range(ITER):
        # for each row in the image we will do the following
        for i in range(rows):
            redTotalSum = sum(r[i])
            greenTotalSum = sum(g[i])
            blueTotalSum = sum(b[i])
            redModulus = redTotalSum % 2
            greenModulus = greenTotalSum % 2
            blueModulus = blueTotalSum % 2

            if(redModulus == 0):
                r[i] = numpy.roll(r[i], Kr[i])
            else:
                r[i] = numpy.roll(r[i], -Kr[i])
            if(greenModulus == 0):
                g[i] = numpy.roll(g[i], Kr[i])
            else:
                g[i] = numpy.roll(g[i], -Kr[i])
            if(blueModulus == 0):
                b[i] = numpy.roll(b[i], Kr[i])
            else:
                b[i] = numpy.roll(b[i], -Kr[i])

    # for each column in the image we will do the following
        for j in range(columns):
            redTotalSum = 0
            greenTotalSum = 0
            blueTotalSum = 0

            for k in range(rows):
                redTotalSum += r[k][j]
                greenTotalSum += g[k][j]
                blueTotalSum += b[k][j]

            redModulus = redTotalSum % 2
            greenModulus = greenTotalSum % 2
            blueModulus = blueTotalSum % 2

            if(redModulus == 0):
                helperModule.upshift(r, j, Kc[j])  # up circular shift
            else:
                helperModule.downshift(r, j, Kc[j])  # down circular shift
            if(greenModulus == 0):
                helperModule.upshift(g, j, Kc[j])  # up circular shift
            else:
                helperModule.downshift(g, j, Kc[j])  # down circular shift
            if(blueModulus == 0):
                helperModule.upshift(b, j, Kc[j])  # up circular shift
            else:
                helperModule.downshift(b, j, Kc[j])  # down circular shift

    # for each row
    for i in range(rows):
        for j in range(columns):
            if(i % 2 == 0):
                r[i][j] = r[i][j] ^ helperModule.rotate180(Kc[j])
                g[i][j] = g[i][j] ^ helperModule.rotate180(Kc[j])
                b[i][j] = b[i][j] ^ helperModule.rotate180(Kc[j])
            else:
                r[i][j] = r[i][j] ^ Kc[j]
                g[i][j] = g[i][j] ^ Kc[j]
                b[i][j] = b[i][j] ^ Kc[j]

    # for each column
    for i in range(columns):
        for j in range(rows):
            if(i % 2 == 0):
                r[j][i] = r[j][i] ^ Kr[j]
                g[j][i] = g[j][i] ^ Kr[j]
                b[j][i] = b[j][i] ^ Kr[j]
            else:
                r[j][i] = r[j][i] ^ helperModule.rotate180(Kr[j])
                g[j][i] = g[j][i] ^ helperModule.rotate180(Kr[j])
                b[j][i] = b[j][i] ^ helperModule.rotate180(Kr[j])

    # assigning encrypted image to the original image
    for i in range(rows):
        for j in range(columns):
            pix[i, j] = (r[i][j], g[i][j], b[i][j])

    # saving the encrypted image to new folder
    im.save('encrypted/encrypted_image.png')
