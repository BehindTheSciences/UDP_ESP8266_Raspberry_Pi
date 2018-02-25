# ili9341 TFT TouchScreen Buttons by BehindTheSciences.com
# Thanks to Brian Lavery

#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so.

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import pyowm
from threading import Timer
import time
from lib_tft24T import TFT24T
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import socket
import spidev
from time import sleep
def draw_rectangle(draw, coordinates, color, width=1):
    for i in range(width):
        rect_start = (coordinates[0][0] - i, coordinates[0][1] - i)
        rect_end = (coordinates[1][0] + i, coordinates[1][1] + i)
        draw.rectangle((rect_start, rect_end), outline = color)
UDP_PORT = 64123
UDP_IP = ""
MESSAGE = "BehindTheSciences.com"
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))
sock.sendto(MESSAGE, ("192.168.1.2", 8888))


# Raspberry Pi configuration.
#For LCD TFT SCREEN:
DC = 24
RST = 25
LED = 15
PEN = 26
#For PEN TOUCH:

# Create TFT LCD/TOUCH object:
TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=False)
# If landscape=False or omitted, display defaults to portrait mode
# This demo can work in landscape or portrait
TFT.initTOUCH(PEN)


# Initialize display.
TFT.initLCD(DC, RST, LED)
# If rst is omitted then tie rst pin to +3.3V
# If led is omitted then tie led pin to +3.3V

# Get the PIL Draw object to start drawing on the display buffer.
draw = TFT.draw()
TFT.clear()
hotspots = [
(0,90,240,160, "0"),    # even the window exit button gets a hotspot !
(0,165,240,240, "1"),
(0,245,240,320, "2")]
image = Image.open('bl1.png')

# Resize the image and rotate it so it's 240x320 pixels.
image = image.rotate(0,0,1).resize((240, 320))
# Draw the image on the display hardware.
print('Drawing image')
d = ImageDraw.Draw(image)
print('Loading image...')
draw_rectangle(d, ((0,90), (240,155)), color=(255,0,0), width=5)
draw_rectangle(d, ((0,165), (240,235)), color=(255,0,0), width=5)
draw_rectangle(d, ((0,245), (240,315)), color=(255,0,0), width=5)

TFT.display(image)
x =255
y = 0
a = 255
b = 0
i =255

start = time.time()

while 1:
#    TFT.clear((255, 0, 0))
    if ((time.time() - start)>20):
	GPIO.output(LED,False)
    # Alternatively can clear to a black screen by simply calling:
#    TFT.clear()
    font = ImageFont.truetype("FreeSans.ttf", 30)
    data, addr = sock.recvfrom(1024)
    print(data)
    d.rectangle([120,5,240,60],fill=(0,160,227))
    d.text((120, 25),data+ chr(176)+ "C",(255,0,0),font=font)
    d.text((120,0),"London",(255,255,0),font=font)
    TFT.display(image)
#    while not TFT.penDown():
#	if ((time.time() - start)>20):
#        	GPIO.output(LED,False)
#        pass
    pos = TFT.penPosition()
    pos = TFT.penPosition()
    pos = TFT.penPosition()
    pos = TFT.penPosition()
    pos = TFT.penPosition()
    pos = TFT.penPosition()
    pos = TFT.penPosition()    # Read corsor position of pen
    if GPIO.input(LED)==0:
	GPIO.output(LED,True)
    	start = time.time()
	continue
    spot = TFT.penOnHotspot(hotspots, pos)
    # So what "button" was clicked by the pen?
    if spot == None:
	start = time.time()
        continue
    if spot == "0":
	print('Button 0 Pressed')
	start = time.time()
        x , y = y , x
	draw_rectangle(d, ((0,90), (240,155)), color=(x,y,0), width=5)
        TFT.display(image)
    if spot == "1":
	print('Button 1 Pressed')
	start = time.time()
	a , b = b , a
	draw_rectangle(d, ((0,165), (240,235)), color=(a,b,0), width=5)
        TFT.display(image)
    if spot == "2":
	print('Button 2 Pressed')
	start = time.time()
        i , j = j , i
        draw_rectangle(d, ((0,245), (240,315)), color=(i,j,0), width=5)
        TFT.display(image)

#        All colours may be any notation (exc for clear() function):
#        (255,0,0)  =red    (R, G, B) - a tuple
#        0x0000FF   =red    BBGGRR   - note colour order
#        "#FF0000"  =red    RRGGBB   - html style
#        "red"      =red    html colour names, insensitive

