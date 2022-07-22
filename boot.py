# boot.py -- run on boot-up
import machine
from network import ETH

# Connect via ethernet
eth = ETH()
eth.init(hostname="itrich-pygate-001")
eth.ifconfig(config="dhcp")

while not eth.isconnected():
    print('.', end='')
    time.sleep(1)
print(" Connected via Ethernet")

# Proceed with main.py
machine.main('main.py')
