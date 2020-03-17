
#include "../inc/StepCtrl.h"
#include "dwt_delay.h"
#include <stdlib.h>

Stepper::Stepper(uint8_t ID){	
    this->divisor = .1125; // 1.8 degrees / 16
	
    if(ID==1) {
        this->scaler = 4.8888;
        this->limitSteps = convertAngleToSteps(350.0);
        this->currentPositionSteps = convertAngleToSteps(175.0);
				this->targetSteps = convertAngleToSteps(175.0);
    } else if (ID==2) {
        this->scaler = 6.85;
			  this->limitSteps = convertAngleToSteps(126.0);
        this->currentPositionSteps = convertAngleToSteps(36.0);
				this->targetSteps = convertAngleToSteps(36.0);
    } else if (ID==3) {
        this->scaler = 6.85;
			  this->limitSteps = convertAngleToSteps(170.0);
        this->currentPositionSteps = convertAngleToSteps(0.0);
				this->targetSteps = convertAngleToSteps(0.0);
    }
		
}

void Stepper::setHome(uint8_t ID) {
    if(ID==1) {
        this->currentPositionSteps = convertAngleToSteps(175.0);
				this->targetSteps = convertAngleToSteps(175.0);
    } else if (ID==2) {
        this->currentPositionSteps = convertAngleToSteps(36.0);
				this->targetSteps = convertAngleToSteps(36.0);
    } else if (ID==3) {
        this->currentPositionSteps = convertAngleToSteps(0);
				this->targetSteps = convertAngleToSteps(0);
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
}

void Stepper::setTarget(uint32_t value){
		this->targetSteps = convertValueToSteps(value);
}

bool  Stepper::goToTarget() {

    if(this->targetSteps > this->limitSteps) {
        return false;
    }
    int tempSteps;
		int tempTarget = this->targetSteps;
		tempSteps = this->targetSteps - this->currentPositionSteps;
    int steps  =  getAbs(tempSteps);
    if (tempSteps < 0) {
        setDirection(false);
    } else {
        setDirection(true);
    }
    int i; 
		HAL_GPIO_WritePin(GPIOA, STEP, GPIO_PIN_SET);
		
		uint32_t delayFAST = 200;
		uint32_t delay = 600;
		

    for(i = 0; i < steps; i++) {
			// the target has been changed during loop
			if(tempTarget != this->targetSteps){
				break;
			}
			
			if( i < steps/2 && delay > delayFAST){
				delay--;
			} else if (i > (steps - 800) ){
				delay++;
			}
        HAL_GPIO_WritePin(GPIOA, STEP, GPIO_PIN_SET);
        DWT_Delay_us(delay);
        HAL_GPIO_WritePin(GPIOA, STEP, GPIO_PIN_RESET);
			  DWT_Delay_us(delay);
	
				this->currentPositionSteps += (1 * this->direction);
    }

    
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

int Stepper::convertAngleToSteps(float angle){
    return (int) ( (angle/this->divisor)*(this->scaler) );
}

int Stepper::convertValueToSteps(uint32_t value){
	  return convertAngleToSteps(convertValueToAngle(value));
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
