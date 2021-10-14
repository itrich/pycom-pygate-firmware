from network import WLAN
import time
import machine
import ujson
from machine import RTC
import pycom

print('\nStarting LoRaWAN concentrator')
# Disable Hearbeat
pycom.heartbeat(False)

# Read secrets file from Filesystem
with open('secret.json','r') as fp:
    secrets = ujson.load(fp)

# Define callback function for Pygate events
def machine_cb (arg):
    evt = machine.events()
    if (evt & machine.PYGATE_START_EVT):
        # Green
        pycom.rgbled(0x103300)
    elif (evt & machine.PYGATE_ERROR_EVT):
        # Red
        pycom.rgbled(0x331000)
    elif (evt & machine.PYGATE_STOP_EVT):
        # RGB off
        pycom.rgbled(0x000000)

# register callback function
machine.callback(trigger = (machine.PYGATE_START_EVT | machine.PYGATE_STOP_EVT | machine.PYGATE_ERROR_EVT), handler=machine_cb)

print('Connecting to WiFi...',  end='')
# Connect to a Wifi Network
wlan = WLAN(mode=WLAN.STA)
wlan.connect(secrets['ssid'], auth=(WLAN.WPA2, secrets['passphrase']))

while not wlan.isconnected():
    print('.', end='')
    pycom.rgbled(0x8800FF)
    time.sleep(0.5)
    pycom.rgbled(0x000000)
    time.sleep(0.5)
print(" OK", end='\n')

print('Connected to', secrets['ssid'], 'with IP', wlan.ifconfig()[0])

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

config['gateway_conf'].update({'gateway_ID': secrets['gateway_ID']})
config['gateway_conf']['servers'][0].update({'gateway_ID': secrets['gateway_ID']})
# Start the Pygate
ujson.dump(buf, config)
machine.pygate_init(buf)
# disable degub messages
# machine.pygate_debug_level(1)
