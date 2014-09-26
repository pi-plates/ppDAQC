import spidev
import time
import string
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

#Initialize
GPIO.setmode(GPIO.BCM)
GPIObaseADDR=8
ppFRAME = 25
ppINT = 22
GPIO.setup(ppFRAME,GPIO.OUT)
GPIO.setup(ppINT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
spi = spidev.SpiDev()
spi.open(0,1)	

MAXADDR=8
	
def CLOSE():
	spi.close()
	GPIO.cleanup()

def Help():
	help()

def HELP():
	help()	
	
def help():
	print ("Analog Input Functions:")
	print ("	getADC(addr, channel) - return voltage")
	print
	print ("Digital Input Functions:")
	print ("	getDINbit(addr,bit) - return bit value")
	print ("	getDINall(addr) - return all eight bits")
	print ("	enableDINint(addr, bit, type) - ")
	print ("	disableDINint(addr,bit)")	
	print
	print ("Digital Output Functions:")	
	print ("	setDOUTbit(addr, bit) - set single bit")
	print ("	clrDOUTbit(addr, bit) - clear single bit")
	print ("	toggleDOUTbit(addr, bit) - toggle a single bit")	
	print ("	setDOUTall(addr,byte) - set all the bits a once")
	print
	print ("Digital to Analog Converter & Pulse Width Modulator Functions:")	
	print ("	setPWM(addr,channel,value)")
	print ("	getPWM(addr,channel)")	
	print ("	setDAC(addr,channel,value)")
	print ("	getDAC(addr,channel)")		
	print
	print ("Bicolor LED control functions:")
	print ("	setLED(addr,color)")
	print ("	clrLED(addr,color)")
	print
	print ("System Level Functions:")	
	print ("	getID(addr) - return descriptor string")
	print ("	getFWrev(addr) - return FW revision in byte format")
	print ("	getHWrev(addr) - return HW revision in byte format")
	print ("	getADDR(addr) - return address of pi-plate. Used for polling available boards")
	print ("  	  at power up.")
	print
	print ("Switch Functions:")
	print ("	getSWstate(addr) - returns current state of on board switch. A value of 1 is")
	print ("	  returned when the switch is up and a value of 0 is returned when it's down.")
	print ("	enableSWpower(addr) - pushing button on ppGPIO will short RPI GPIO pin X to") 
	print ("  	  GND and then remove 5VDC 45 seconds later. Note that this setting is saved")
	print ("  	  in nonvolatile memory and only has to be performed once")
	print ("	disableSWpower(addr) - disables the above. Note that this setting is stored")
	print ("   	  in nonvolatile memory and only has to be performed once.")
	print ("	enableSWint(addr) - allows the switch to generate an interrupts when pressed.")
	print ("	  Global interrupts must be enabled before using this function.")
	print ("	disableSWint(addr) - blocks switch on board from generating an interrupt.")
	
	print 
	print ("getINTflags(addr, int) - returns then clears all INT flags ")
	print
	print ("Definitions:")
	print ("    Address (addr): ppDAQC boards have jumpers on the board that allow")
	print ("      their address to be set to a value between 0 and 7.")
	print ("    ADC (analog to digital converter) channels can be 0 through 8 for a ")
	print ("      total of 9 channels. Reading channel 8 will return the power supply")
	print ("      voltage.")
	print ("    DIN (digital input) channels can be 0 through 7 for a total of 8 channels")
	print ("    DOUT (digital output) channels can be 0 through 6 for a total of 7 channels")
	print ("    PWM (pulse width modulator) channels can be 0 or 1 for a total of 2")
	print ("       channels. The output values can be between 0 and 1023.")
	print ("      ")
	print ("    DAC (digital to analog converter) channels can be 0 or 1 for a total of")
	print ("      2 channels. The output value can be between 0 and 4.096 volts")
#===============================================================================#	
# ADC Functions	     	                                              			#
#===============================================================================#	
def getADC(addr,channel):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (channel>8):
		return "ERROR: channel argument out of range - must be less than 9"	
	resp=ppCMD(addr,0x30,channel,0,2)
	value=(256*resp[0]+resp[1])
	#print value
	value=round(value*4.096/1024,3)
	#print value
	if (channel==8):
		value=value*2.0
	return value

#===============================================================================#	
# Digital Input Functions	                                                   	#
#===============================================================================#
def getDINbit(addr,bit):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>7):
		return "ERROR: bit argument out of range"
	resp=ppCMD(addr,0x20,bit,0,1)
	if resp[0] > 0:
		return 1
	else:
		return 0
		
def getDINall(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x25,0,0,1)
	return resp[0]

def enableDINint(addr, bit, edge):	# enable DIN interrupt
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>7):
		return "ERROR: bit argument out of range"	
	if ((edge=='f') or (edge=='F')):
		resp=ppCMD(addr,0x21,bit,0,0)		
	if ((edge=='r') or (edge=='R')):
		resp=ppCMD(addr,0x22,bit,0,0)
	if ((edge=='b') or (edge=='B')):
		resp=ppCMD(addr,0x23,bit,0,0)		
		
def disableDINint(addr,bit):	# disable DIN interrupt
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>7):
		return "ERROR: bit argument out of range"
	resp=ppCMD(addr,0x24,bit,0,0)
	
#===============================================================================#	
# LED Functions	                                                   		   		#
#===============================================================================#			
def setLED(addr,led):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (led>1):
		return "Error: invalid LED value"
	resp=ppCMD(addr,0x60,led,0,0)

def clrLED(addr,led):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1	
	if (led>1):
		return "Error: invalid LED value"
	resp=ppCMD(addr,0x61,led,0,0)

def toggleLED(addr,led):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1	
	if (led>1):
		return "Error: invalid LED value"
	resp=ppCMD(addr,0x62,led,0,0)	

def getLED(addr,led):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1	
	if (led>1):
		return "Error: invalid LED value"
	resp=ppCMD(addr,0x63,led,0,1)
	return resp[0]	


#==============================================================================#	
# Switch Functions	                                                   #
#==============================================================================#		
def getSWstate(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x50,0,0,1)
	return resp[0]

def enableSWint(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x51,0,0,0)

def disableSWint(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x52,0,0,0)		
	
def enableSWpower(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x53,0,0,0)

def disableSWpower(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
		resp=ppCMD(addr,0x54,0,0,0)
		
		
#==============================================================================#	
# Digital Output Functions	                                                   #
#==============================================================================#	
def setDOUTbit(addr,bit):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>6):
		return "ERROR: bit argument out of range - must be less than 7"
	resp=ppCMD(addr,0x10,bit,0,0)

	
def clrDOUTbit(addr,bit):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>6):
		return "ERROR: bit argument out of range - must be less than 7"
	resp=ppCMD(addr,0x11,bit,0,0)		

def toggleDOUTbit(addr,bit):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (bit>6):
		return "ERROR: bit argument out of range - must be less than 7"
	resp=ppCMD(addr,0x12,bit,0,0)		
	
def setDOUTall(addr,byte):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (byte>127):
		return "ERROR: byte argument out of range - must be less than 128"
	resp=ppCMD(addr,0x13,byte,0,0)			

def getDOUTbyte(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x14,0,0,1)
	return resp


#==============================================================================#	
# PWM and DAC Output Functions	                                                   #
#==============================================================================#	
def setPWM(addr,channel,value):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (value>1023):
		return "ERROR: PWM argument out of range - must be less than 1024"
	if (channel>2):
		return "Error: PWM channel must be 0 or 1"
	hibyte = value>>8
	lobyte = value - (hibyte<<8)
	resp=ppCMD(addr,0x40+channel,hibyte,lobyte,0)

def getPWM(addr,channel):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (channel>2):
		return "Error: PWM channel must be 0 or 1"
	## Return PWM set value
	
	
def setDAC(addr,channel,value):
	global Vcc
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (value>4.097):
		return "ERROR: PWM argument out of range - must be less than 4.097 volts"
	if (channel>2):
		return "Error: PWM channel must be 0 or 1"
	value = int(value/Vcc[addr]*1024)
	hibyte = value>>8
	lobyte = value - (hibyte<<8)
	resp=ppCMD(addr,0x40+channel,hibyte,lobyte,0)

	
def getDAC(addr,channel):
	global Vcc
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	if (value>4.097):
		return "ERROR: PWM argument out of range - must be less than 4.097 volts"
	if (channel>2):
		return "Error: PWM channel must be 0 or 1"
	## Return DAC value
	resp=ppCMD(addr,0x40+channel+2,0,0,2)
	value=(256*resp[0]+resp[1])
	return resp


#==============================================================================#	
# Interrupt Control Functions	                                               #
#==============================================================================#	
def intEnable(addr):	#ppDAQC will pull down on INT pin if an enabled event occurs
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x04,0,0,0)
	
def intDisable(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x05,0,0,0)
	
def getINTflags(addr):	#read INT flag registers in ppDAQC
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x06,0,0,2)
	value=(256*resp[0]+resp[1])
	return value
		
#==============================================================================#	
# System Functions	                                                   		   #
#==============================================================================#	
def getFWrev(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x03,0,0,1)
	rev = resp[0]
	whole=float(rev>>4)
	point = float(rev&0x0F)
	return whole+point/10.0
	
def getHWrev(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x02,0,0,1)
	rev = resp[0]
	whole=float(rev>>4)
	point = float(rev&0x0F)
	return whole+point/10.0	

def getADDR(addr):
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0x00,0,0,1)
	return resp[0]
	
def getID(addr):
	global GPIObaseADDR
	addr=addr+GPIObaseADDR
	if (addr>255):
		return "ERROR: address out of range - must be less than 255"
	id=""
	arg = range(4)
	resp = []
	arg[0]=addr;
	arg[1]=0x1;
	arg[2]=0;
	arg[3]=0;

	ppFRAME = 25
	GPIO.output(ppFRAME,True)
	null = spi.writebytes(arg)
	count=0
	time.sleep(.0001)
	while (count<20): 
		dummy=spi.readbytes(1)
		if (dummy[0] != 0):
			num = dummy[0]
			id = id + chr(num)
			count = count + 1
		else:
			count=20
	GPIO.output(ppFRAME,False)
	return id	
	
def getPROGdata(addr,paddr):	#read INT flag registers in ppDAQC
	if (addr>MAXADDR):
		return "ERROR: address out of range - must be less than", MAXADDR-1
	resp=ppCMD(addr,0xF0,paddr>>8,paddr&0xFF,2)
	value=(256*resp[0]+resp[1])
	return hex(value)	
	
def ppCMD(addr,cmd,param1,param2,bytes2return):
	global GPIObaseADDR
	arg = range(4)
	resp = []
	arg[0]=addr+GPIObaseADDR;
	arg[1]=cmd;
	arg[2]=param1;
	arg[3]=param2;
	#print arg
	GPIO.output(ppFRAME,True)
	null = spi.writebytes(arg)
	if bytes2return>0:
		time.sleep(.0001)
		for i in range(0,bytes2return):	
			dummy=spi.readbytes(1)
			resp.append(dummy[0])
	GPIO.output(ppFRAME,False)
	return resp	
	

	
Vcc=range(8)
ppFoundCount=0
#getID(0)
for i in range (0,8):
	rtn = getADDR(i)
	if ((rtn-8)==i):
		Vcc[i] = getADC(i,8)
		setDOUTall(i,0)
		setPWM(i,0,0)
		setPWM(i,1,0)
		ppFoundCount += 1
	else:
		Vcc[i]=10000

print ppFoundCount,"ppDAQC boards found"

# GPIO Commands
# Common:
# * Return ADDR: 0xF0
# * Return INT status: 0xF1 - will return at least two bytes
# DIO:
 # * Generate ppINT on falling edge of input: 0x00-0x07
 # * Generate ppINT on rising edge of input: 0x08-0x0F
 # * Set Bit to Output: 0x10-0x17
 # * Set Bit to Input: 0x18-0x1F
 # * Set Output bit high: 0x28-0x2F
 # * Set Output bit low: 0x20-0x27
 # * Read Input bit: 0x30-0x37 - returns a single byte
 # * Disable ppINT on input: 0x38-0x3F

 # * Open Collector:
 # * Turn on bit: 0x48-0x4E   note that there are only 7 OC lines
 # * Turn off bit: 0x40-0x47
 # * Toggle bit: 0x50-0x57
 # * Write all bits: 0x58, dd - where dd is less than 128

 # A/D:
 # * Read channel: 0x60-0x67 - returns two, right justified bytes with MSB first
 # * Read all channels: 0x68 - returns channels 0 - 7 as ten bytes

 # DAC:
 # * Set value: 0b111000mm,0bllllllll where m are the MSBs and the ls are the LSBs.


 # Switches:
 # * Generate ppINT on closure of switch: 0x90-0x91
 # * Disable ppINT on switch: 0x98-0x99

 
#Command format 
#	Byte 1: pp Address
#	Byte 2: Instruction
#		Bits 7-4: Class
#		Bits 3-0: Command
#	Byte 3: Parameter 1
#	Byte 4: Parameter 2

# GPIO Commands
# Command Type: 0
# System:
# * Return ADDR: 0x00
# * No parameters (NULL is RCVD)
# * Response should be address of device if present
#
# * Return INT status: 0x01 
# * No Parameters
# * will return one byte to reflect DIO and a 2nd to reflect buttons

# Command Type: 1
# Open Collector:
# Subcommands:
# 	Turn on bit: 0
#	Turn off bit: 1
#	Toggle bit:	2
#	Write Byte: 3
#1st parameter:
#	Bit number for subcommands 0 thru 2 (must be between 0 and 6) or byte value for subcommand 3 (<128)

# Command Type: 2
# A/D:
# Subcommands:
# 	Read one channel: 0
# 	Read all channels: 1
# 1st parameter:
#	Channel number if applicable
# Returns:
# 	Unsigned 16 bit integer MSB first for single channel read
# 	Eight 16 bit integers for the all channel read


 # DAC:
 # * Set value: 0b111000mm,0bllllllll where m are the MSBs and the ls are the LSBs.

# setLED
# cmds:
	# 0: Turn on
	# 1: Turn off
	# 2: Toggle
	# 3: Read value
# led:
	# 0: RED
	# 1: GREEN

# Command Type: 7
# Switches:
# Subcommands:
# 	Read switch status: 0 
#		returns a byte with status of both switches.
# 	Generate ppINT on closure of switch: 1
#	Disable ppINT on switch: 2
#1st parameter (only applicable for ppINT settings):
#	Specific Switch
#		0: Switch 1
#		1: Switch 2
# Note that an A/D read takes about 25 microseconds. Therefore there should be a delay between the commands and the retrieval of data.
 
 