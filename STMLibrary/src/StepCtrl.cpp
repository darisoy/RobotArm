
#include "../inc/StepCtrl.h"


Stepper::Stepper(){
    setMode(1);
}


void  Stepper::setHome(){


}

void Stepper::returnToHome(){

}


void  Stepper::setMode(uint8_t mode){
    HAL_GPIO_WritePin(GPIOB, M2, GPIO_PIN_SET);
    HAL_GPIO_WritePin(GPIOB, M1, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, M0, GPIO_PIN_RESET);
    this->stepResolution = 16; 
    this->divisor = 1.8/stepResolution;
}

 
void  Stepper::setPosition(float angle){
    int steps = calculateSteps(angle);
    int delay = 1;
    int i;
    for(i=0; i<steps; i++){
        HAL_GPIO_WritePin(GPIOA, STEP, GPIO_PIN_SET);
        HAL_Delay(delay);
        HAL_GPIO_WritePin(GPIOA, STEP, GPIO_PIN_RESET);
        HAL_Delay(delay);
    }
}

void Stepper::setDirection(bool dir){
	if(dir){
        HAL_GPIO_WritePin(GPIOB, DIR, GPIO_PIN_SET);
    } else {
        HAL_GPIO_WritePin(GPIOB, DIR, GPIO_PIN_RESET);
    }
}

float Stepper::getPosition(){

	return 0.0;
}

void  Stepper::enable(bool){


}

void  Stepper::disable(bool){


}

/** PRIVATE FUNCTIONS **/

int Stepper::calculateSteps(float angle){
    return (int) (angle/this->divisor);
}
