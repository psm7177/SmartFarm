#RPi Pinouts

#I2C Pins 
#GPIO2 -> SDA
#GPIO3 -> SCL

#Import the Library Requreid 
import smbus
import time
import struct

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
#Slave Address 1
address = 0x04

#Slave Address 2

WRITE = 0
READ = 1
WRITE_REGIST = 2
READ_REGIST= 3

class WriteModule:
    MOTOR = 0

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
        self.MotorControll(1,1,1);
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
    def MotorControll(self,a,b,c):
        bus.write_i2c_block_data(address,WRITE,[WriteModule.MOTOR,self.IN1,self.IN2,self.ENA,a,b,c])
    def regist(self):
        print("Regist\n")
        bus.write_i2c_block_data(address,WRITE_REGIST,[WriteModule.MOTOR,self.IN1,self.IN2,self.ENA])

class Temperature:
    def __init__(self,address,pin):
        self.address = address
        self.pin = pin
        self.regist()
    def regist(self):
        bus.write_i2c_block_data(address,READ_REGIST,[ReadModule.TEMPERATURE,self.pin])
    def read(self):
        bus.write_i2c_block_data(address,READ,[ReadModule.TEMPERATURE,self.pin])
        time.sleep(1)
        result = bus.read_i2c_block_data(address,0,8)
        humidity = CharArraytoFloat(result[0:4])
        temperature =  CharArraytoFloat(result[4:9])
        return temperature,humidity

def CharArraytoFloat(Array):
    print(len(Array))
    return struct.unpack('f',struct.pack('BBBB',Array[0],Array[1],Array[2],Array[3]))[0]
        
#a = bus.read_i2c_block_data(address,0,256)

# motor = Motor(address,7,8,9)
# motor.stop()

temperature = Temperature(address,2)
a = temperature.read()

#temperature.read()


#End of the Script