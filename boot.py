# boot.py -- run on boot-up
import machine
import pycom
from _pybytes import Pybytes
from _pybytes_config import PybytesConfig

# Enable Pybytes
pybytes_conf = PybytesConfig().read_config()
pybytes = Pybytes(pybytes_conf)
pybytes.start()

# Proceed with main.py
machine.main('main.py')
