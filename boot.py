# boot.py -- run on boot-up
import machine
import pycom

# We want to save a little bit power
# Disable Heartbeat LED
pycom.heartbeat_on_boot(False)
# Proceed with main.py
machine.main('main.py')
