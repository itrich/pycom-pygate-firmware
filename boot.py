# boot.py -- run on boot-up
import machine
import time
# from network import ETH
from network import WLAN

# # Connect via ethernet
# eth = ETH()
# eth.init(hostname="itrich-pygate-001")
# eth.ifconfig(config="dhcp")
#
# while not eth.isconnected():
#     print('.', end='')
#     time.sleep(1)
# print(" Connected via Ethernet")

# Connect via wifi
wlan = WLAN(mode=WLAN.STA)
wlan.connect(ssid='Ed', auth=(WLAN.WPA2, '20221123'))

while not wlan.isconnected():
    print('.', end='')
    time.sleep(1)
print(" Connected via WiFi")

# Proceed with main.py
machine.main('main.py')
