
import os
import glob
import time
import RPi.GPIO as GPIO
import lcddriver

GPIO.setmode(GPIO.BCM)

pinlist = [4, 5, 6, 17, 27]

for i in pinlist:
	GPIO.setup(i, GPIO.OUT)
GPIO.output(5,GPIO.HIGH)
GPIO.output(6,GPIO.HIGH)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = lcddriver.lcd()

display.lcd_display_string("Testing", 1)

Try:
while True:
	print(read_temp())
	time.sleep(1)
	if read_temp() > (20,86): 
		GPIO.output(17,GPIO.LOW)
		GPIO.output(27,GPIO.HIGH)
		GPIO.output(5,GPIO.LOW)	
		print("HVAC ON")
		
	else:	
		GPIO.output(27,GPIO.LOW)
		GPIO.output(17,GPIO.HIGH)
		GPIO.output(5,GPIO.HIGH)
		print("HVAC OFF")
		
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    display.lcd_clear()
    GPIO.cleannup()

