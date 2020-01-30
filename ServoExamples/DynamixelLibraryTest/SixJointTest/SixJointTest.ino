/*******************************************************************************
* Copyright 2016 ROBOTIS CO., LTD.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

#include <Dynamixel2Arduino.h>

#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_MEGA2560)
  #include <SoftwareSerial.h>
  SoftwareSerial soft_serial(7, 8); // DYNAMIXELShield UART RX/TX
  #define DXL_SERIAL   Serial
  #define DEBUG_SERIAL soft_serial
  const uint8_t DXL_DIR_PIN = 2; // DYNAMIXEL Shield DIR PIN
#else
  #define DXL_SERIAL   Serial1
  #define DEBUG_SERIAL Serial
  const uint8_t DXL_DIR_PIN = 2; // DYNAMIXEL Shield DIR PIN
#endif

const uint8_t FOREARM = 4;
const uint8_t WRIST = 5;
const float DXL_PROTOCOL_VERSION = 2.0;
int x = A0;    
int y = A1; 
int z = A2;
int STEPx = 2;
int DIRx = 5;
int STEPy = 3;
int DIRy = 6;
int STEPz = 4;
int DIRz = 7;
int EN = 8;
int DELAY = 100; //microseconds

Dynamixel2Arduino dxl(DXL_SERIAL, DXL_DIR_PIN);

void setup() {
  /****************************************
   *       DYNAMIXEL SERVO SETUP          *
   * **************************************/

  // Use UART port of DYNAMIXEL Shield to debug.
  DEBUG_SERIAL.begin(115200);
  // Set Port baudrate to 57600bps. This has to match with DYNAMIXEL baudrate.
  dxl.begin(57600);
  // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  // Get DYNAMIXEL information
  dxl.ping(FOREARM);
  // Turn off torque when configuring items in EEPROM area
  dxl.torqueOff(FOREARM);
  dxl.setOperatingMode(FOREARM, OP_POSITION);
  dxl.torqueOn(FOREARM);
  dxl.torqueOff(WRIST);
  dxl.setOperatingMode(WRIST, OP_POSITION);
  dxl.torqueOn(WRIST);


  /****************************************
   *           STEPPER SETUP              *
   * **************************************/

  pinMode(STEPx, OUTPUT);
  pinMode(DIRx, OUTPUT);
  pinMode(STEPy, OUTPUT);
  pinMode(DIRy, OUTPUT);
  pinMode(STEPz, OUTPUT);
  pinMode(DIRz, OUTPUT);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, HIGH);
}

void motion(int x, int y, int z);
int joyStick(int val);


void loop() {

  motion(joyStick(analogRead(x)), joyStick(analogRead(y)), joyStick(analogRead(z)) );
  //dxl.setGoalPosition(FOREARM, 512);
  //dxl.setGoalPosition(WRIST, 512);
  //delay(1000);

  // Set Goal Position in DEGREE value
  //dxl.setGoalPosition(FOREARM, 5.7, UNIT_DEGREE);
  //dxl.setGoalPosition(WRIST, 5.7, UNIT_DEGREE);
  //delay(1000);

}


void motion(int x, int y, int z){
  switch(x){
    case 0: delayMicroseconds(DELAY*2);
            break;
    case 1: //Serial.println("Down");
            digitalWrite(DIRx, HIGH);
            digitalWrite(STEPx, HIGH);
            delayMicroseconds(DELAY);
            digitalWrite(STEPx, LOW);
            delayMicroseconds(DELAY);
            break;
    case 2: //Serial.println("Up");
            digitalWrite(DIRx, LOW);
            digitalWrite(STEPx, HIGH);
            delayMicroseconds(DELAY);
            digitalWrite(STEPx, LOW);
            delayMicroseconds(DELAY);
            break;
  }
  switch(y){
    case 0: delayMicroseconds(DELAY*2);
            break;
    case 1: digitalWrite(DIRy, HIGH);
            digitalWrite(STEPy, HIGH);
            delayMicroseconds(DELAY);
            digitalWrite(STEPy, LOW);
            delayMicroseconds(DELAY);
            break;
    case 2: digitalWrite(DIRy, LOW);
            digitalWrite(STEPy, HIGH);
            delayMicroseconds(DELAY);
            digitalWrite(STEPy, LOW);
            delayMicroseconds(DELAY);
            break;
  }
   switch(z){
    case 0: delayMicroseconds(DELAY*2);
            break;
    case 1: digitalWrite(DIRz, HIGH);
            digitalWrite(STEPz, HIGH);
            delayMicroseconds(DELAY);
            digitalWrite(STEPz, LOW);
            delayMicroseconds(DELAY);
            break;
    case 2: digitalWrite(DIRz, LOW);
            digitalWrite(STEPz, HIGH);
            delayMicroseconds(DELAY);
            digitalWrite(STEPz, LOW);
            delayMicroseconds(DELAY);
            break;
  }
}

// 0 = Nothing, 1 = (-), 2 = (+)
int joyStick(int val){
  if(val<200){
    return 1;
  } else if(val>600){
    return 2;
  } else {
    return 0;
  }
}
