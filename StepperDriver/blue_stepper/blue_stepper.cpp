
#include "blue_stepper.h"
#include <Arduino.h>


BlueStepper::BlueStepper(){
    
    //assign pins
    this->DIR = PB12;
    this->STEP = PB13;
    this->M2 = PB14;
    this->M1 = PB15;
    this->M0 = PA8;
    this->EN = PA9;
    pinMode(this->STEP,OUTPUT); 
    pinMode(this->DIR,OUTPUT);
    setMode(0,0,0); //default

    
}


void  BlueStepper::setHome(){


}

void BlueStepper::returnToHome(){

}

/************* Microstepping Indexer *******************
 * Mode2 | Mode1 | Mode0  |   Step Mode
 *   0   |   0   |   0    |   Full Step    
 *   0   |   0   |   1    |   Half Step   
 *   0   |   1   |   0    |   1/4 Step   
 *   0   |   1   |   1    |   1/8 Step   
 *   1   |   0   |   0    |   1/16 Step   
 *   1   |   0   |   1    |   1/32 Step
 * ****************************************************/

void  BlueStepper::setMode(int m2, int m1, int m0){
    this->M2 = m2;
    this->M1 = m1;
    this->M0 = m0;
    this->stepResolution = (1<<((int) ((m2<<2) | (m1<<1) | (m0<<0) ))) ;
    this->divisor = 1.8/stepResolution;
}

 
void  BlueStepper::setPosition(float angle){

    int steps = calculateSteps(angle);
    int i;
    for(i=0; i<steps; i++){
        Serial.println("In set position");
        digitalWrite(this->STEP, HIGH);
        delayMicroseconds(1000);
        digitalWrite(this->STEP, LOW);
        delayMicroseconds(1000); 
    }
}

float BlueStepper::getPosition(){


}

void  BlueStepper::enable(bool){


}

void  BlueStepper::disable(bool){


}

/** PRIVATE FUNCTIONS **/

int BlueStepper::calculateSteps(float angle){
    return (int) (angle/this->divisor);
}
