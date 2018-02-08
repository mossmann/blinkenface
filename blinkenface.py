#!/usr/bin/python

import skidl

skidl.lib_search_paths[skidl.KICAD].append('gsg-kicad-lib')

gnd = skidl.Net('GND')
vcc = skidl.Net('VCC')

num_leds = 242
leds = []
sdo = []
cko = []
for i in range(num_leds):
	leds.append(skidl.Part('gsg-symbols.lib', 'APA102', footprint='gsg-modules:APA102-2020'))
	sdo.append(skidl.Net('SDO' + str(i)))
	cko.append(skidl.Net('CKO' + str(i)))
	leds[i]['SDI'] += sdo[i]
	leds[i]['CKI'] += cko[i]
	leds[i]['GND'] += gnd
	leds[i]['VCC'] += vcc
	# connect input to previous output
	if 0 < i:
		leds[i-1]['SDO'] += sdo[i]
		leds[i-1]['CKO'] += cko[i]

# don't connect the output of the last LED
leds[-1]['SDO'] += NC
leds[-1]['CKO'] += NC

# connect the input of the first LED to a pin header
header = skidl.Part('conn', 'CONN_01X04', footprint='gsg-modules:HEADER-1x4')
header[1] += gnd
header[2] += vcc
header[3] += cko[0]
header[4] += sdo[0]

# assume that power is applied to pin header
header[1].net.drive = skidl.POWER
header[2].net.drive = skidl.POWER

decoupling_caps = []
decoupling_caps.append(skidl.Part('device', 'C', footprint='gsg-modules:0805'))
decoupling_caps.append(skidl.Part('device', 'C', footprint='gsg-modules:0603'))
for i in range(2):
	decoupling_caps[i][1] += vcc
	decoupling_caps[i][2] += gnd

skidl.ERC()
skidl.generate_netlist()
