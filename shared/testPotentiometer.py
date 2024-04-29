import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import time
import sys
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Read and print the voltage and value of the potentiometer
while(True):
    sys.stdout.write("\033[2K\033[1G")  # Clear the current line and move cursor to beginning
    sys.stdout.write("Voltage: {:.2f}V".format(abs(chan.voltage)))  # Write new output to the same line
    sys.stdout.flush()  # Force Python to write out everything in the buffer
    time.sleep(0.2)
