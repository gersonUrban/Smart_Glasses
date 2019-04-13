import picamera
import time
import os
from gtts import gTTS
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep
from gpiozero import Button
from subprocess import Popen


GPIO.setmode(GPIO.BCM)

# Take a picture Button
GPIO.setup(5,GPIO.IN, pull_up_down=GPIO.PUD_UP)
# function + Button
GPIO.setup(6,GPIO.IN, pull_up_down=GPIO.PUD_UP)
# function - Button
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Volume up Button
GPIO.setup(19,GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Volume down Button
GPIO.setup(26,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#button = GPIO.input(18)
camera = picamera.PiCamera()
#button = Button(18)
#button = Button(27)
#button = Button(22)


function = 0
volume = 50
PATH_IMAGE = 'images/'
IMAGE_NAME = 'image.png'
PATH_FUNCTIONS = 'functions/'
functions_dict = {
'0': 'leitor_de_textos.mp3',
'1': 'leitor_de_cedulas.mp3',
'2': 'leitor_de_baralho.mp3',
'3': 'leitor_de_cores.mp3',
'4': 'leitor_de_ambiente.mp3',
'5': 'identificador_de_pessoas.mp3',
'6': 'identificador_de_produtos.mp3',
'7': 'cadastro_de_pessoa.mp3'
}


def take_photo():
    camera.start_preview(alpha=190)
    sleep(1)
    camera.capture(PATH_IMAGE+IMAGE_NAME)
    camera.stop_preview()
    
def increase_volume():
    Popen(['amixer', 'set', 'PCM', '100%+'])#0.01%+
    #Popen('amixer sset Master 1%')
def decrease_volume():
    Popen(['amixer', 'set', 'PCM', '100%-'])
    #Popen('amixer sset Master 1%')

while True:
    input_take_photo = GPIO.input(26)
    input_function_up = GPIO.input(19)
    input_function_down = GPIO.input(5)#13
    input_volume_up = GPIO.input(13)#6
    input_volume_down = GPIO.input(6)#5
    
    if input_take_photo == False:
        take_photo()
        if function == 0:
            print(functions_dict[str(function)])
        elif function == 1:
            print(functions_dict[str(function)])
        elif function == 2:
            print(functions_dict[str(function)])
        elif function == 3:
            print(functions_dict[str(function)])
        elif function == 4:
            print(functions_dict[str(function)])
        elif function == 5:
            print(functions_dict[str(function)])
        elif function == 6:
            print(functions_dict[str(function)])
        elif function == 7:
            print(functions_dict[str(function)])
        time.sleep(0.2)
    
    if input_function_up == False:
        if function < 7:
            function += 1
        else:
            function = 0
        
        aud = "mpg321 "+PATH_FUNCTIONS+functions_dict[str(function)]
        os.system(aud)
        print(aud)
        time.sleep(0.2)
        
    if input_function_down == False:
        if function > 0:
            function -= 1
        else:
            function = 7
        
        aud = "mpg321 "+PATH_FUNCTIONS+functions_dict[str(function)]
        os.system(aud)
        print(aud)
        time.sleep(0.2)
        
    if input_volume_up == False:
        increase_volume()
        print('volume incrised')
        time.sleep(0.1)
        
    if input_volume_down == False:
        decrease_volume()
        print('volume decrised')
        time.sleep(0.1)
