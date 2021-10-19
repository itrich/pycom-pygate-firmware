# boot.py -- run on boot-up
import machine
import pycom
from _pybytes import Pybytes
from _pybytes_config import PybytesConfig

# We want to save a little bit power
# Disable Heartbeat LED
pycom.heartbeat_on_boot(False)
# Enable Pybytes
pybytes_conf = PybytesConfig().read_config()
pybytes = Pybytes(pybytes_conf)
pybytes.start()

# disable debug messages
machine.pygate_debug_level(1)

# Proceed with main.py
machine.main('main.py')
