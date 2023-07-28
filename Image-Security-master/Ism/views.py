"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from Ism import app
from flask import request
import random
import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from flask import send_file
from PIL import Image
from random import randint
import numpy
import sys
from helper import *
from PIL import Image
from random import randint
import numpy
import sys
from helper import *
from PIL import Image
from math import sqrt
import cv2 as cv2

Kr = []
Kc = []


def encrypt(file):
    global Kr, Kc
    # im = Image.open(r"C:\Users\DELL\Desktop\ISM\Ism_Epj\Image-Security-master\taj.png")
    im = Image.open(
        r"C:\Users\DELL\Desktop\ISM\Ism_Epj_Final\{f}".format(f=file))
    pix = im.load()
    # Obtaining the RGB matrices
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

    m = im.size[0]
    n = im.size[1]

    # Vectors Kr and Kc
    alpha = 8
    Kr = [randint(0, pow(2, alpha)-1) for i in range(m)]
    Kc = [randint(0, pow(2, alpha)-1) for i in range(n)]
    ITER_MAX = 1

    print('Vector Kr : ', Kr)
    print('Vector Kc : ', Kc)

    f = open('keys.txt', 'w+')
    f.write('Vector Kr : \n')
    for a in Kr:
        f.write(str(a) + '\n')
    f.write('Vector Kc : \n')
    for a in Kc:
        f.write(str(a) + '\n')
    f.write('ITER_MAX : \n')
    f.write(str(ITER_MAX) + '\n')

    for iterations in range(ITER_MAX):
        # For each row
        for i in range(m):
            rTotalSum = sum(r[i])
            gTotalSum = sum(g[i])
            bTotalSum = sum(b[i])
            rModulus = rTotalSum % 2
            gModulus = gTotalSum % 2
            bModulus = bTotalSum % 2
            if(rModulus == 0):
                r[i] = numpy.roll(r[i], Kr[i])
            else:
                r[i] = numpy.roll(r[i], -Kr[i])
            if(gModulus == 0):
                g[i] = numpy.roll(g[i], Kr[i])
            else:
                g[i] = numpy.roll(g[i], -Kr[i])
            if(bModulus == 0):
                b[i] = numpy.roll(b[i], Kr[i])
            else:
                b[i] = numpy.roll(b[i], -Kr[i])
        # For each column
        for i in range(n):
            rTotalSum = 0
            gTotalSum = 0
            bTotalSum = 0
            for j in range(m):
                rTotalSum += r[j][i]
                gTotalSum += g[j][i]
                bTotalSum += b[j][i]
            rModulus = rTotalSum % 2
            gModulus = gTotalSum % 2
            bModulus = bTotalSum % 2
            if(rModulus == 0):
                upshift(r, i, Kc[i])
            else:
                downshift(r, i, Kc[i])
            if(gModulus == 0):
                upshift(g, i, Kc[i])
            else:
                downshift(g, i, Kc[i])
            if(bModulus == 0):
                upshift(b, i, Kc[i])
            else:
                downshift(b, i, Kc[i])
        # For each row
        for i in range(m):
            for j in range(n):
                if(i % 2 == 1):
                    r[i][j] = r[i][j] ^ Kc[j]
                    g[i][j] = g[i][j] ^ Kc[j]
                    b[i][j] = b[i][j] ^ Kc[j]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kc[j])
                    g[i][j] = g[i][j] ^ rotate180(Kc[j])
                    b[i][j] = b[i][j] ^ rotate180(Kc[j])
        # For each column
        for j in range(n):
            for i in range(m):
                if(j % 2 == 0):
                    r[i][j] = r[i][j] ^ Kr[i]
                    g[i][j] = g[i][j] ^ Kr[i]
                    b[i][j] = b[i][j] ^ Kr[i]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kr[i])
                    g[i][j] = g[i][j] ^ rotate180(Kr[i])
                    b[i][j] = b[i][j] ^ rotate180(Kr[i])

    for i in range(m):
        for j in range(n):
            pix[i, j] = (r[i][j], g[i][j], b[i][j])

    im.save(r"C:\Users\DELL\Desktop\ISM\Ism_Epj_Final\Image-Security-master\Ism\static\content\Encrypted.png")
    return (Kr, r"C:\Users\DELL\Desktop\ISM\Ism_Epj_Final\Image-Security-master\Ism\static\content\Encrypted.png")
    # fo=open("enc.jpg","wb")
    # imageRes="enc.jpg"
    # fo.write(image)
    # fo.close()
    # return (key,imageRes)


def decrypt(key, file):
    global Kr, Kc
    im = Image.open(
        r"C:\Users\DELL\Desktop\ISM\Ism_Epj_Final\Image-Security-master\Ism\static\content\Encrypted.png")
    pix = im.load()

    # Obtaining the RGB matrices
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

    m = im.size[0]
    n = im.size[1]

    # Kr = []
    # Kc = []

    # print('Enter value of Kr')

    # for i in range(m):
    #     Kr.append(int(input()))

    # print('Enter value of Kc')
    # for i in range(n):
    #     Kc.append(int(input()))

    # print('Enter value of ITER_MAX')
    # ITER_MAX = int(input())

    for iterations in range(1):
        # For each column
        for j in range(n):
            for i in range(m):
                if(j % 2 == 0):
                    r[i][j] = r[i][j] ^ Kr[i]
                    g[i][j] = g[i][j] ^ Kr[i]
                    b[i][j] = b[i][j] ^ Kr[i]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kr[i])
                    g[i][j] = g[i][j] ^ rotate180(Kr[i])
                    b[i][j] = b[i][j] ^ rotate180(Kr[i])
        # For each row
        for i in range(m):
            for j in range(n):
                if(i % 2 == 1):
                    r[i][j] = r[i][j] ^ Kc[j]
                    g[i][j] = g[i][j] ^ Kc[j]
                    b[i][j] = b[i][j] ^ Kc[j]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kc[j])
                    g[i][j] = g[i][j] ^ rotate180(Kc[j])
                    b[i][j] = b[i][j] ^ rotate180(Kc[j])
        # For each column
        for i in range(n):
            rTotalSum = 0
            gTotalSum = 0
            bTotalSum = 0
            for j in range(m):
                rTotalSum += r[j][i]
                gTotalSum += g[j][i]
                bTotalSum += b[j][i]
            rModulus = rTotalSum % 2
            gModulus = gTotalSum % 2
            bModulus = bTotalSum % 2
            if(rModulus == 0):
                downshift(r, i, Kc[i])
            else:
                upshift(r, i, Kc[i])
            if(gModulus == 0):
                downshift(g, i, Kc[i])
            else:
                upshift(g, i, Kc[i])
            if(bModulus == 0):
                downshift(b, i, Kc[i])
            else:
                upshift(b, i, Kc[i])

        # For each row
        for i in range(m):
            rTotalSum = sum(r[i])
            gTotalSum = sum(g[i])
            bTotalSum = sum(b[i])
            rModulus = rTotalSum % 2
            gModulus = gTotalSum % 2
            bModulus = bTotalSum % 2
            if(rModulus == 0):
                r[i] = numpy.roll(r[i], -Kr[i])
            else:
                r[i] = numpy.roll(r[i], Kr[i])
            if(gModulus == 0):
                g[i] = numpy.roll(g[i], -Kr[i])
            else:
                g[i] = numpy.roll(g[i], Kr[i])
            if(bModulus == 0):
                b[i] = numpy.roll(b[i], -Kr[i])
            else:
                b[i] = numpy.roll(b[i], Kr[i])

    for i in range(m):
        for j in range(n):
            pix[i, j] = (r[i][j], g[i][j], b[i][j])

    im.save(r"C:\Users\DELL\Desktop\ISM\Ism_Epj_Final\Image-Security-master\Ism\static\content\Decrypted.png")
    return r"C:\Users\DELL\Desktop\ISM\Ism_Epj_Final\Image-Security-master\Ism\static\content\Decrypted.png"
    # fo=open("dec.jpg","wb")
    # imageRes="dec.jpg"
    # fo.write(image)
    # fo.close()
    # return imageRes


def correlation():

    value_of_x = 0
    value_of_y = 0

    # color_index_of_rgb 0-red,1-green,2-blue

    def co1(color_index_of_rgb, height, width, pixels):
        value = 0
        for pixel_coordinate_of_y in range(0, height):
            for pixel_coordinate_of_x in range(0, width):
                if pixel_coordinate_of_x+1 == width:
                    break
                value = pixels[pixel_coordinate_of_x, pixel_coordinate_of_y][color_index_of_rgb] * \
                    pixels[pixel_coordinate_of_x+1,
                           pixel_coordinate_of_y][color_index_of_rgb]+value

        return value*height*width

    def co2(color_index_of_rgb, height, width, pixels):
        global value_of_y
        global value_of_x
        for pixel_coordinate_of_y in range(0, height):
            for pixel_coordinate_of_x in range(0, width):
                if pixel_coordinate_of_x+1 == width:
                    break
                value_of_x = pixels[pixel_coordinate_of_x,
                                    pixel_coordinate_of_y][color_index_of_rgb]+value_of_x
                value_of_y = pixels[pixel_coordinate_of_x+1,
                                    pixel_coordinate_of_y][color_index_of_rgb]+value_of_y

        return value_of_x*value_of_y

    def co3(color_index_of_rgb, height, width, pixels):
        value = 0
        for pixel_coordinate_of_y in range(0, height):
            for pixel_coordinate_of_x in range(0, width):
                value = (pixels[pixel_coordinate_of_x,
                                pixel_coordinate_of_y][color_index_of_rgb])**2 + value

        xy = (value*height*width)-(value_of_x**2)
        return xy

    def co4(color_index_of_rgb, height, width, pixels):
        value = 0
        for pixel_coordinate_of_y in range(0, height):
            for pixel_coordinate_of_x in range(0, width):
                if pixel_coordinate_of_x+1 == width:
                    break
                value = (pixels[pixel_coordinate_of_x+1,
                                pixel_coordinate_of_y][color_index_of_rgb]**2)+value

        xy = (value*height*width)-(value_of_y**2)
        return xy

    def corr_of_rgb(loc):
        global value_of_y
        global value_of_x
        photo = Image.open(loc)
        # cryptotiger.bmp
        pixels = photo.load()
        width, height = photo.size
        value_of_y = 0
        value_of_x = 0
        r = ((co1(0, height, width, pixels)-co2(0, height, width, pixels)) /
             sqrt(co3(0, height, width, pixels)*co4(0, height, width, pixels)))
        value_of_y = 0
        value_of_x = 0
        g = ((co1(1, height, width, pixels) - co2(1, height, width, pixels)) /
             sqrt(co3(1, height, width, pixels) * co4(1, height, width, pixels)))
        value_of_x = 0
        value_of_y = 0
        b = ((co1(2, height, width, pixels) - co2(2, height, width, pixels)) /
             sqrt(co3(2, height, width, pixels) * co4(2, height, width, pixels)))

        ans = (r+g+b)/3
        return ans

    enc = corr_of_rgb(
        r"C:\Users\DELL\Desktop\ISM\Ism_Epj_Final\Image-Security-master\Ism\static\content\Encrypted.png")
    dnc = corr_of_rgb(
        r"C:\Users\DELL\Desktop\ISM\Ism_Epj_Final\Image-Security-master\Ism\static\content\Decrypted.png")
    return (enc, dnc)


def Entropy():
    def entropy(im):
        # Compute normalized histogram -> p(g)
        p = numpy.array([(im == v).sum() for v in range(256)])
        p = p/p.sum()
        # Compute e = -sum(p(g)*log2(p(g)))
        e = -(p[p > 0]*numpy.log2(p[p > 0])).sum()

        return e
    
    enc=entropy(cv2.imread(
    r'C:\Users\DELL\Desktop\ISM\Ism_Epj_Final\Image-Security-master\Ism\static\content\Encrypted.png'))
    dnc=entropy(cv2.imread(
    r'C:\Users\DELL\Desktop\ISM\Ism_Epj_Final\Image-Security-master\Ism\static\content\Decrypted.png'))
    return (enc,dnc)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Decrypt',
        year=datetime.now().year,
        message='Upload your encrypted image along with the key'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='Encrypt',
        year=datetime.now().year,
        message='Upload the image here'
    )


@app.route('/contact1', methods=['POST'])
def contact1():
    if request.method == 'POST':
        global f
        f = request.files['file']
        f.save(f.filename)
        text = request.form['key']
        key = int(text)
        image = decrypt(key, f.filename)
        return render_template('contact1.html',
                               title='Decrypted',
                               year=datetime.now().year,
                               message='This is your Decrypted image', name=f.filename)


@app.route('/about1', methods=['POST'])
def about1():
    if request.method == 'POST':
        global f
        f = request.files['file']
        f.save(f.filename)
        key, image = encrypt(f.filename)
        return render_template('about1.html',
                               title='Encrypted',
                               year=datetime.now().year,
                               message='This is your encrypted image', name=f.filename, keys=key, images=image)


@app.route('/cor', methods=['GET'])
def cor():
    if request.method == 'GET':
        global f
        #f = request.files['file']
        # f.save(f.filename)
        enc, dnc = correlation()
        return render_template('cor.html',
                               title='Correlation',
                               year=datetime.now().year,
                               message='This is your correlation values of  Image', keys=enc, images=dnc)


@app.route('/ent', methods=['GET'])
def ent():
    if request.method == 'GET':
        global f
        #f = request.files['file']
        # f.save(f.filename)
        enc, dnc = Entropy()
        return render_template('ent.html',
                               title='Entropy',
                               year=datetime.now().year,
                               message='This is your Entropy values of  Image', keys=enc, images=dnc)


@app.route('/return-file')
def return_file():
    return send_file("../enc.jpg", attachment_filename="enc.jpg")


@app.route('/return-file1')
def return_file1():
    return send_file("../dec.jpg", attachment_filename="dec.jpg")
