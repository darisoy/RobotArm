#include <blue_stepper.h>

BlueStepper s = BlueStepper(PB13, PB12);

void setup() {
  //s.setPosition(30);
  pinMode(PB13,OUTPUT); 
  pinMode(PB12,OUTPUT);
  s.setMode(0,0,0);
}
void loop() {
  s.setPosition(360);
  delay(1000);
}
