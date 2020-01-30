

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
int DELAY = 50; //microseconds

void setup() {
  Serial.begin(9600);
  pinMode(STEPx, OUTPUT);
  pinMode(DIRx, OUTPUT);
  pinMode(STEPy, OUTPUT);
  pinMode(DIRy, OUTPUT);
  pinMode(STEPz, OUTPUT);
  pinMode(DIRz, OUTPUT);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, HIGH);
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

void loop() {
  motion(joyStick(analogRead(x)), joyStick(analogRead(y)), joyStick(analogRead(z)) );
}
