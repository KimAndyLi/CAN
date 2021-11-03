# from __future__ import print_function
 
import can
import pandas as pd
import cantools
import binascii
import time
 
def recieve_msgs():
    bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
    while True:
        timeout=5
        messages = bus.recv(timeout=None)
        id = messages.arbitration_id
        data = messages.data
        current_time=time.time()
        # print(time.time())
        
        if id == 35:
            print('VCVCCU: ONLINE')
        elif id != 35:
            print('VCVCCU: OFFLINE')
            
            
        if id == 36:
            print('PUMPOT: ONLINE')
        elif id != 36:
            print('PUMPOT: OFFLINE')
 
recieve_msgs()