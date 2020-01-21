#include <DHT.h>
#include <DHT_U.h>
#include <Servo.h>

//Import the library required

#include <Wire.h>

char Temperature_Index[5];
DHT* Temperature_Array[5];

char Servo_Index[5];
Servo* Servo_Array[5];

//Slave Address for the Communication
#define SLAVE_ADDRESS 0x04

char recv_buffer[32];
char send_buffer[32];

enum TYPE
{
  WRITE,
  READ,
  WRITE_REGIST,
  READ_REGIST
};

enum WriteModule
{
  MOTOR,
  SERVO
};

enum ReadModule
{
  Temperature
};


void Write()
{
  switch(recv_buffer[1])
  {
    case MOTOR:
      ControllMotor(recv_buffer[2],recv_buffer[3],recv_buffer[4],recv_buffer[5],recv_buffer[6],recv_buffer[7]);
      break;
    case SERVO:
      ControllServo(recv_buffer[2],recv_buffer[3]);
      break;
  }  
}

void WriteRegist()
{
    switch(recv_buffer[1])
  {
    case MOTOR:
      RegistMotor(recv_buffer[2],recv_buffer[3],recv_buffer[4]);
      break;
    case SERVO:
      RegistServo(recv_buffer[2]);
      break;
  }  
}

void Read()
{
  switch(recv_buffer[1])
  {
    case Temperature:
      ReadTemperature(recv_buffer[2]);
  }
}

void ReadRegist()
{
  switch(recv_buffer[1])
  {
    case Temperature:
      RegistTemperature(recv_buffer[2]);
      break;
  }
}

void RegistMotor(char in1Pin,char in2Pin,int enaPin)
{
  pinMode(in1Pin,OUTPUT);
  pinMode(in2Pin,OUTPUT);
  pinMode(enaPin,OUTPUT);
}

void ControllMotor(char in1Pin,char in2Pin,int enaPin, char val_in1, char val_in2, char val_ena)
{
  digitalWrite(in1Pin,val_in1);
  digitalWrite(in2Pin,val_in2);
  digitalWrite(enaPin,val_ena);
}

void RegistTemperature(char pin)
{
  for(int i = 0; i < 5; i++)
  {
    if(Temperature_Index[i]== -1)
    {
      Temperature_Array[i] = new DHT(pin,DHT11);
      Temperature_Array[i]->begin();
      Temperature_Index[i] = pin;
      return;
    }else if(Temperature_Index[i]== pin) return;
  }
}
void ReadTemperature(char readPin)
{
  char TempBuffer[9] = "";
  for(int i = 0; i < 5 ;i ++)
  {
    if(Temperature_Index[i]==readPin)
    {
      float humidity = Temperature_Array[i]->readHumidity();
      float temperature = Temperature_Array[i]->readTemperature();
      Serial.println(humidity);
      memcpy(TempBuffer,&humidity,sizeof(float));
      memcpy(TempBuffer+4,&temperature,sizeof(float));
    }
  }
  TempBuffer[8]='\0';
  memcpy(send_buffer,TempBuffer,9);
}

void RegistServo(char pin)
{
  for(int i = 0; i < 5; i++)
  {
    if(Servo_Index[i]== -1)
    {
      Servo_Array[i] = new Servo();
      Servo_Array[i]->attach(pin);
      Servo_Index[i] = pin;
      return;
    }else if(Servo_Index[i]== pin) return;
  }
}
void ControllServo(char ControllPin,char angle)
{
  for(int i = 0; i < 5 ;i ++)
  {
    if(Servo_Index[i]==ControllPin)
    {
      Servo_Array[i]->write(angle);
    }
  }
}

//Code Initialization
void setup() {
  // initialize i2c as slave
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  memset(Temperature_Array,0,sizeof(DHT*)*5);
  memset(Temperature_Index,-1,sizeof(char)*5);
  
  memset(Servo_Array,0,sizeof(Servo*)*5);
  memset(Servo_Index,-1,sizeof(char)*5);
}

void loop() 
{
  for(int i = 0 ; i < 5; i++)
  {
    //Serial.println((int)Temperature_Index[i]);
    if(Temperature_Index[i]!=-1)
    {
      float h = Temperature_Array[i]->readTemperature();
      //Serial.println(h);
    }
  }
  delay(1000);
}

// callback for received data
void receiveData(int byteCount) {
  memset(recv_buffer,0,32);
  int i = 0;
  Serial.print("Input: ");
  
  while (Wire.available()) {
    recv_buffer[i] = Wire.read();
    Serial.print((int)recv_buffer[i]);
    i++;
  }
  recv_buffer[i] = '\0';
  
  switch(recv_buffer[0])
  {
    case WRITE:
      Write();
      break;
    case READ:
      Read();
      break;
    case WRITE_REGIST:
      WriteRegist();
      break;
    case READ_REGIST:
      ReadRegist();
      break;
  }
}  // end while

// callback for sending data
void sendData() 
{
  Wire.write(send_buffer,32);
  memset(send_buffer,0,32);
}
