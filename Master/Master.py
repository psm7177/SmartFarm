import smbus
import time
import struct

from threading import Thread

bus = smbus.SMBus(1)

address = 0x04

WRITE = 0
READ = 1
WRITE_REGIST = 2
READ_REGIST= 3

ReadModuleArray = []

class WriteModule:
    MOTOR = 0
    SERVO = 1
class ReadModule:
    TEMPERATURE = 0
class Motor:
    STOP = 0
    CW = 1
    CCW = 2
    def __init__(self,address,IN1,IN2,ENA1):
        self.state = self.STOP
        self.address = address
        self.IN1 = IN1
        self.IN2 = IN2
        self.ENA = ENA1
        self.regist()
    def stop(self):
        self.controll(1,1,1);
        # bus.write_byte_data(address,self.IN1,0)
        # bus.write_byte_data(address,self.IN2,0)
        # bus.write_byte_data(address,self.ENA1,0)
        self.state = self.STOP

    def CW(self):
        # bus.write_byte_data(address,self.IN1,1)
        # bus.write_byte_data(address,self.IN2,0)
        # bus.write_byte_data(address,self.ENA1,1)
        self.state = self.CW

    def CCW(self):
        # bus.write_byte_data(address,self.IN1,0)
        # bus.write_byte_data(address,self.IN2,1)
        # bus.write_byte_data(address,self.ENA1,1)
        self.state = self.CCW

    def controll(self,a,b,c):
        bus.write_i2c_block_data(address,WRITE,[WriteModule.MOTOR,self.IN1,self.IN2,self.ENA,a,b,c])
    def regist(self):
        print("Regist\n")
        bus.write_i2c_block_data(address,WRITE_REGIST,[WriteModule.MOTOR,self.IN1,self.IN2,self.ENA])

class Temperature:
    def __init__(self,address,pin):
        self.address = address
        self.pin = pin
        self.regist()
        #numpy 
        #numpy
        ReadModuleArray.append(self)
    def regist(self):
        bus.write_i2c_block_data(address,READ_REGIST,[ReadModule.TEMPERATURE,self.pin])
    def read(self):
        bus.write_i2c_block_data(address,READ,[ReadModule.TEMPERATURE,self.pin])
        time.sleep(1)
        result = bus.read_i2c_block_data(address,0,8)
        humidity = CharArraytoFloat(result[0:4])
        temperature =  CharArraytoFloat(result[4:9])
        return temperature,humidity

class Servo:
    def __init__(self, address,pin):
        self.address = address
        self.pin = pin
        self.angle = 0
        self.regist()
    def regist(self):
        bus.write_i2c_block_data(address,WRITE_REGIST,[WriteModule.SERVO,self.pin])
        self.controll(0)
    def controll(self,angle):
        self.angle = angle
        bus.write_i2c_block_data(address,WRITE,[WriteModule.SERVO,self.pin,angle])

def CharArraytoFloat(Array):
    print(len(Array))
    return struct.unpack('f',struct.pack('BBBB',Array[0],Array[1],Array[2],Array[3]))[0]

def ReadSystem():
    while True:
        for  Module in ReadModuleArray:
            Module.read()
        time.sleep(20)

if __name__ == '__main__':
    Thread(target=readSystem, name="",daemon=True).start()
    print("Master.py")

#a = bus.read_i2c_block_data(address,0,256)

# motor = Motor(address,7,8,9)
# motor.stop()

#temperature = Temperature(address,2)
#a = temperature.read()
#temperature.read()