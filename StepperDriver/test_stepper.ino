#include <blue_stepper.h>
const int stepPin = PB13; 
const int dirPin = PB12;

BlueStepper s = BlueStepper();

void setup() {
  s.setMode(0,0,0);
}
void loop() {
  s.setPosition(360);
  delay(1000);
}
