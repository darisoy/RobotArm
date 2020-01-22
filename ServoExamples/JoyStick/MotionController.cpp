#include "AccelStepper.h"
#include "MultiStepper.h"

#define STEP0 2
#define STEP1 3
#define STEP2 4
#define DIR0  5
#define DIR1  6
#define DIR2  7
#define ENABLE 8

AccelStepper arm_array[6];
MultiStepper group_array;
const int AXES = 3;
// arm_array[4] = AccelStepper(AccelStepper::DRIVER, XSTEP, XDIR); // Servo: Shoulder
// arm_array[5] = AccelStepper(AccelStepper::DRIVER, YSTEP, YDIR); // Servo: Arm     
// arm_array[6] = AccelStepper(AccelStepper::DRIVER, ZSTEP, ZDIR); // Servo: Wrist

void motion_setup(void) {
	Serial.begin(9600); 

	// Pin map setup for each stepper function
	// AccelStepper sets pinMode as well.
	arm_array[0] = AccelStepper(AccelStepper::DRIVER, STEP0, DIR0); // Stepper: Shoulder
	arm_array[1] = AccelStepper(AccelStepper::DRIVER, STEP1, DIR1); // Stepper: Arm     
	arm_array[2] = AccelStepper(AccelStepper::DRIVER, STEP2, DIR2); // Stepper: Wrist

	// set max speed and acc for each stepper and add it to the group class.
	for (int i = 0; i < AXES; i++) {
		arm_array[i].setMaxSpeed(100);
		arm_array[i].setAcceleration(25.0);
		group_array.addStepper(arm_array[i]);
	}

	pinMode(ENABLE, OUTPUT);
	digitalWrite(ENABLE, LOW);

	Serial.println("Setup Complete");
}

void test_motors(void) {
    long coords0[3] = { 10 * 328, 10 * 328, 4 * 328 };
    long coords1[3] = { 10 * -328, 10 * -328, 4 * -328 };

    steppers.moveTo(coords0);
    steppers.runSpeedToPosition();
    delay(100);
    
    zero_motors();
    delay(100);
    
    steppers.moveTo(coords1);
    steppers.runSpeedToPosition();
    delay(100);
    
    zero_motors();
    delay(100);
}

void zero_motors(void) {
	for (int i = 0; i < AXES; i += 1) {
		arm_array[i].setCurrentPosition(0);
	}
}