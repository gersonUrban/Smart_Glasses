#em vez de ler e salvar o texto todo, ler e salvar as frases
#separar em mais módulo, tipo, ocr, leitor...

#from PIL import Image # Importando o módulo Pillow para abrir a imagem no script
#from Pillow import Image, ImageFilter
import pytesseract # Módulo para a utilização da tecnologia OCR
from gtts import gTTS
import shutil
#from skimage.io import imread
#import skimage.filters
from scipy.optimize import curve_fit

from matplotlib import pyplot as plt

import os
import math
import imutils
import numpy as np
import matplotlib.pylab as plt
#from PIL import Image, ImageFilter

#import cv2 as cv
from numpy.polynomial.polynomial import polyfit





PATH = 'pipeline/'
PATH_CROP = PATH+'croped/'
PATH_CROP2 = PATH+'croped2/'
#PATH_UNSHARP = 'croped_unsharped/'
PATH_IMAGE = PATH + 'pdf2img/'
PATH_TXT = PATH + 'text/'

KERNEL_W, KERNEL_H = 5,100 



def image_standard(img, im_name, PATH_IMAGE):
    # Reading image
    im = Image.open(PATH_IMAGE+img)

    # Getting RGB average value of image
    color = im.resize((1, 1)).getpixel((0, 0))

    # Applying Unsharp to highligth text
    #im = im.filter(ImageFilter.UnsharpMask(radius=8, percent=150))

    # Get im Name
    #im_name = PATH_IMAGE.split('.')
    #im_name = im_name[0]+'_300.'+im_name[1]

    # Save image
    print("saving: "+im_name)
    im.save(im_name, dpi=(300,300))

def get_im_name(img, PATH_IMAGE):
    # Get im Name
    im_name = (PATH_IMAGE+img).split('.')
    im_name = im_name[0]+'_300.'+im_name[1]
    return im_name

def get_ctrs(im_name):
    image = cv.imread(im_name)

    #Rotacionar a imagem geral, afim de pegar certo..
    #usar o centro de massa, talvez, ou a mesma ideia..
    #grayscale
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    #binary
    ret,thresh = cv.threshold(gray,127,255,cv.THRESH_BINARY_INV)
    #dilation
    kernel = np.ones((KERNEL_W,KERNEL_H), np.uint8)
    img_dilation = cv.dilate(thresh, kernel, iterations=1)
    #find contours
    ctrs, hier = cv.findContours(img_dilation.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    print(len(ctrs))
    return ctrs


def save_croped_images(im_name, ctrs, PATH_CROP):
    
    image = cv.imread(im_name)
    
    #Removing all files in folder
    r = os.listdir(PATH_CROP)
    for i in r:
        os.remove(PATH_CROP+i)
        os.remove(PATH_CROP2+i)
    
    for i, ctr in enumerate(ctrs):

        image2 = image.copy()
        #Transform image in binary image # Pode dar problemas...
        ret,image2 = cv.threshold(image2,127,255,cv.THRESH_BINARY)

        # If is another countor, delete from image
        for j, c in enumerate(ctrs):
            if j != i:
                cv.drawContours(image2, [c], -1, (255,255,255), -1)

        # Get crop window
        crop = cv.boundingRect(ctr)
        x1 = crop[0]
        x2 = crop[0]+crop[2]
        y1 = crop[1]
        y2 = crop[1]+crop[3]
        #Get Cropped image
        cropped = image2[y1:y2, x1:x2]

        #Finding angle to rotate image
        a = [i[0] for i in ctr]
        x = [i[0] for i in a]
        y = [i[1] for i in a]
        b, m = polyfit(x, y, 1)
        y0 = (b * 0) + m
        y1 = (b * 1) + m
        alpha = math.tan(y1 - y0)
        #Rotate cropped image
        rotated = imutils.rotate_bound(cropped, alpha)

        n = "{:05d}".format(i)
        #Saving cropped images (rotated and non rotated)
        cv.imwrite(PATH_CROP+'crop_'+n+'.png', cropped)
        cv.imwrite(PATH_CROP2+'crop_'+n+'.png', rotated)

def get_text(PATH_CROP,PATH_CROP2):
    files = os.listdir(PATH_CROP)
    files = sorted(files, reverse=True)

    final_text = ''
    for file in files:
        text = pytesseract.image_to_string(Image.open(PATH_CROP+file), lang='por')
        if text != '':
            text = text.replace('\n',' ')
            #display(text)
        else:
            text = pytesseract.image_to_string(Image.open(PATH_CROP2+file), lang='por')
            if text != '':
                print('- ',end='')
                text = text.replace('\n',' ')
                #display(text)
        if len(text) > 0:
            if len(final_text) > 0:
                if final_text[len(final_text) - 1] == '-':
                    final_text = final_text[:-1]+text
                else:
                    final_text += '\n'+text
            else:
                final_text += '\n'+text
                
    return final_text

imgs = os.listdir(PATH_IMAGE)
imgs = sorted(imgs, reverse=True)

for i, img in enumerate(imgs):

    im_name = get_im_name(img, PATH_IMAGE)
    print(im_name)
    image_standard(img, im_name, PATH_IMAGE)
    ctrs = get_ctrs(im_name)
    save_croped_images(im_name, ctrs, PATH_CROP)
    text = get_text(PATH_CROP,PATH_CROP2)

    file = open(PATH_TXT+img.split('.')[0]+'.txt','w')
    file.write(text)
    file.close()

pytesseract.image_to_string(Image.open(PATH_IMAGE), lang='por')
tts = gTTS(text=final_text, lang='pt')
tts.save("final_text.mp3")
os.system("mpg321 final_text.mp3")
