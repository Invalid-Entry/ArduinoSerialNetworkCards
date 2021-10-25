from tuntap import Packet, TunTap
from time import sleep, thread_time
from _thread import start_new_thread

import serial
import sys

counter = 0

def outbound(tun, ser, counter):
    while not tun.quitting:
        p = tun.read()
        if not p:
            continue

        packet = Packet(data=p)

        if not packet.get_version()==4:
            continue

        print(''.join('{:02x} '.format(x) for x in packet.data))
        
        print(">", end="")
        # counter += 1
        # if counter >= 10:
        #     print()
        #     counter =0

        ser.write(packet.data)

        sleep(.1)



def inbound(tun, ser, counter):
    while not tun.quitting:
        if (ser.in_waiting > 4):
            bytebuf = []
            data = ser.read(4)
            
            bytebuf.extend(data)

            bytestoRead = int.from_bytes([bytebuf[2], bytebuf[3]], "big") -4

            print("want to read %s" % bytestoRead)

            if (ser.in_waiting < bytestoRead):
                # This is bad, this is open to a DOS attack!
                sleep(.1)
            
            
            data = ser.read(bytestoRead)

            print("<", end="")

            # counter += 1
            # if counter >= 10:
            #     print()
            #     counter =0
            bytebuf.extend(data)
            
            print(''.join('{:02x} '.format(x) for x in bytebuf))

            res = tun.write(bytes(bytebuf))
            print(res)
            sleep(0.1)
        else:
            sleep(0.01)



ip = sys.argv[1]
device = sys.argv[2]

tun = TunTap(nic_type="Tun",nic_name="testtun0")
tun.config(ip=ip,mask="255.255.255.0") #,gateway="192.168.1.254")

ser = serial.Serial(device, 38400, timeout=1)
ser.flushInput()

start_new_thread(outbound, (tun, ser, counter,))
start_new_thread(inbound, (tun, ser, counter,))

while True:
    data = sys.stdin.read(1)
    if data:
        break



#input("press return key to quit!")
tun.close()
ser.close()

#tun.down()
#tun.close()

