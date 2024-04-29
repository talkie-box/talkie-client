import os
import time
import sys
import logging
from daemonize import Daemonize
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('/var/log/volumed.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Function to set volume
def set_volume(vol):
    # Adjust the command to specify the correct card and device
    os.system(f"amixer -c 1 set Speaker playback {vol}%")

def current_volume_percent(voltage):
    return int((voltage / 3.3) * 100)

# Read the voltage and adjust volume
def adjust_volume():
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the ADC object using the I2C bus
    ads = ADS.ADS1115(i2c)

    # Create single-ended input on channel 0
    chan = AnalogIn(ads, ADS.P0)
    currentPercent = current_volume_percent(abs(chan.voltage))

    while True:
        try:
            voltage = abs(chan.voltage)
            volume = int((voltage / 3.3) * 100)  # Assuming 3.3V corresponds to 100% volume    
            if (volume != currentPercent):
                 currentPercent = current_volume_percent(voltage)
                 currentVolume = volume
                 set_volume(volume)
                 logger.debug(f"Set volume to {volume}% for voltage {voltage:.2f}V")
        except Exception as e:
            logger.error("Failed to read voltage or set volume", exc_info=True)
        time.sleep(0.2)

# Daemon
pid = "/tmp/volumed.pid"
daemon = Daemonize(app="volumed", pid=pid, action=adjust_volume, keep_fds=[file_handler.stream.fileno()])
daemon.start()

