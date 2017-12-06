#!/usr/bin/python

# GreatFET -> blinkenface connections
# GND      -> GND
# VBUS     -> VCC
# SCK      -> CKI
# MOSI     -> SDI

from greatfet import GreatFET             
from greatfet.protocol import vendor_requests
import bitstring
import time
import math

start_frame = bitstring.Bits('0x00000000')
end_frame = bitstring.Bits('0xffffffff')

gf = GreatFET()
gf.vendor_request_out(vendor_requests.SPI_INIT)

def led_frame(red=0, green=0, blue=0, brightness=0x1f):
	frame = bitstring.Bits(length=3, uint=0x7)
	frame += bitstring.Bits(length=5, uint=(brightness & 0x1f))
	frame += bitstring.Bits(length=8, uint=(blue & 0xff))
	frame += bitstring.Bits(length=8, uint=(green & 0xff))
	frame += bitstring.Bits(length=8, uint=(red & 0xff))
	return frame

def set2pixels(red1=0, blue1=0, green1=0, red2=0, blue2=0, green2=0):
	data = start_frame
	data += led_frame(red1, blue1, green1)
	data += led_frame(red2, blue2, green2)
	data += end_frame
	#print(data)
	gf.vendor_request_out(vendor_requests.SPI_WRITE, data=data.bytes)

# two pixel test pattern
def test2pixels():
	while(True):
		set2pixels(1, 0, 0, 0, 1, 0)
		time.sleep(0.2)
		set2pixels(0, 1, 0, 0, 0, 1)
		time.sleep(0.2)
		set2pixels(0, 0, 1, 1, 0, 0)
		time.sleep(0.2)

# 242 pixel test pattern
def test242pixels():
	brightness = 1
	period = 22.0
	pixels = bitstring.BitStream()
	for i in range(242):
		red = int(127+127*math.cos(2*math.pi*(i/period)))
		green = int(127+127*math.cos(2*math.pi*((i+period/3)/period)))
		blue = int(127+127*math.cos(2*math.pi*((i+2*period/3)/period)))
		pixels += led_frame(red, green, blue, brightness)
	while(True):
		data = start_frame
		data += pixels
		data += end_frame
		#print(data)
		gf.vendor_request_out(vendor_requests.SPI_WRITE, data=data.bytes)
		time.sleep(0.1)
		pixels.ror(32)

test242pixels()
