
#include "../inc/StepCtrl.h"
#include "dwt_delay.h"
#include <stdlib.h>

Stepper::Stepper(uint8_t ID){
    if(ID==1) {
        this->scaler = 4.8888;
        this->limit = convertAngleToValue(350.0);
	    this->currentPositionAngle = 175.0;
        this->currentPositionSteps = 7604;
    } else if (ID==2) {
        this->scaler = 6.85;
        this->limit = convertAngleToValue(126);
        this->currentPositionAngle = 36.0; 
        this->currentPositionSteps = 2192; 
    } else if (ID==3) {
        this->scaler = 6.85;
        this->limit = convertAngleToValue(170);
        this->currentPositionAngle = 0; 
        this->currentPositionSteps = 0; 
    }
}

void Stepper::setHome(uint8_t ID) {
    if(ID==1) {
				this->currentPositionAngle = 175.0;
				this->currentPositionSteps = 7604;
    } else if (ID==2) {
        this->currentPositionAngle = 36.0;
        this->currentPositionSteps = 7604;
    } else if (ID==3) {
        this->scaler = 6.85;
        this->limit = convertAngleToValue(170);
        this->currentPositionAngle = 0; 
        this->currentPositionSteps = 0; 
    }
}

void Stepper::returnToHome() {

}

/*  For now, this will be locked in at 16th step resolution.
 *
 */
void  Stepper::setMode() {
    HAL_GPIO_WritePin(ENABLE_Port, ENABLE, GPIO_PIN_RESET);
		HAL_GPIO_WritePin(GPIOB, M2, GPIO_PIN_SET);
    HAL_GPIO_WritePin(GPIOB, M1, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, M0, GPIO_PIN_RESET);
    this->stepResolution = 16; 
    this->divisor = .1125; // 1.8 degrees / 16
}

 
bool  Stepper::setPosition(uint32_t value) {

    if(value > this->limit) {
        return false;
    }
    int stepsFromZero = calculateSteps(convertValueToAngle(value));
    int tempSteps;
		tempSteps = stepsFromZero - this->currentPositionSteps;
    int steps  =  getAbs(tempSteps);
    if (tempSteps < 0) {
        setDirection(false);
    } else {
        setDirection(true);
    }
    uint32_t delay = 400;
    int i; 
		HAL_GPIO_WritePin(GPIOA, STEP, GPIO_PIN_SET);

    for(i = 0; i < steps; i++) {
        HAL_GPIO_WritePin(GPIOA, STEP, GPIO_PIN_SET);
        DWT_Delay(delay);
        HAL_GPIO_WritePin(GPIOA, STEP, GPIO_PIN_RESET);
        DWT_Delay(delay);
    }
    /*
    if magnetic encoder says position is off:
        move until position is right
    */
	this->currentPositionSteps += (steps * this->direction);
    
    return true;
}

void Stepper::setDirection(bool dir){
	if (dir) {
        HAL_GPIO_WritePin(GPIOB, DIR, GPIO_PIN_SET);
        this->direction = 1;
    } else {
        HAL_GPIO_WritePin(GPIOB, DIR, GPIO_PIN_RESET);
        this->direction = -1;
    }
}

float Stepper::getPosition() { 
	return 0.0;
}

void  Stepper::enable(bool) {

}

void  Stepper::disable(bool) {

}

/** PRIVATE FUNCTIONS **/

int Stepper::calculateSteps(float angle){
    return (int) ( (angle/this->divisor)*(this->scaler) );
}

float Stepper::convertValueToAngle(uint32_t value){
    return (float) (0.087890625 * value); // 90 degrees corresponds to 1024;
}

float Stepper::getCurrentAngle(){
    return (float) (this->currentPositionSteps * this->divisor)/(this->scaler);
}

uint16_t Stepper::convertAngleToValue(float angle){
    return (uint16_t) (angle/0.087890625);
}

int Stepper::getAbs(int val){
    return (val < 0 ) ? (val * -1) : (val); 
}
