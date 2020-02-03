#include <BlueStepper.h>
// const int stepPin = PB13; 
// const int dirPin = PB12;

BlueStepper s = BlueStepper();

void setup() {
  s.setMode(1,0,0);
}
void loop() {
  s.setPosition(90);
  delay(1000);
}
