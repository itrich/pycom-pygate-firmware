from network import WLAN
import binascii
import time
import machine
import ujson
from machine import RTC
import pycom

# Set Gateway EUI if not already set
if not 'gateway_eui' in pybytes_conf.keys():
    wl = WLAN()
    gateway_eui = binascii.hexlify(wl.mac().sta_mac)[:6] + 'fffe' + binascii.hexlify(wl.mac().sta_mac)[6:]
    pybytes.set_config(key='gateway_eui', value=gateway_eui, permanent=True, silent=False, reconnect=False)

print('\nStarting LoRaWAN concentrator')

# Define callback function for Pygate events
def machine_cb (arg):
    evt = machine.events()
    if (evt & machine.PYGATE_START_EVT):
        # Green
        pycom.rgbled(0x103300)
        pybytes.send_signal(0, 'Start')
    elif (evt & machine.PYGATE_ERROR_EVT):
        # Red
        pycom.rgbled(0x331000)
        pybytes.send_signal(0, 'Error')
    elif (evt & machine.PYGATE_STOP_EVT):
        # RGB off
        pycom.rgbled(0x000000)
        pybytes.send_signal(0, 'Stop')

# register callback function
machine.callback(trigger = (machine.PYGATE_START_EVT | machine.PYGATE_STOP_EVT | machine.PYGATE_ERROR_EVT), handler=machine_cb)

# Sync time via NTP server for GW timestamps on Events
print('Syncing RTC via ntp...', end='')
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

while not rtc.synced():
    print('.', end='')
    time.sleep(.5)
print(" OK", end='\n')

# Read the GW config file from Filesystem
with open('config.json','r') as fp:
    config = ujson.load(fp)

config['gateway_conf'].update({'gateway_ID': pybytes_conf['gateway_eui']})
config['gateway_conf']['servers'][0].update({'gateway_ID': pybytes_conf['gateway_eui']})

# Start the Pygate
machine.pygate_init(ujson.dumps(config))
