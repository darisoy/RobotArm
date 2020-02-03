/**
*********************************************************************************************************
* @file           : StepCtrl.h
* @brief          : This file contains the Stepper class which directly controls
*                   the DRV8825 stepper driver. 
* @date           : 1/29/2020
* @authors        : J. Brandon Iams
*
*
*------ Microstepping Indexer ---------
* Mode2 | Mode1 | Mode0  |   Step Mode
*   0   |   0   |   0    |   Full Step    
*   0   |   0   |   1    |   Half Step   
*   0   |   1   |   0    |   1/4 Step   
*   0   |   1   |   1    |   1/8 Step   
*   1   |   0   |   0    |   1/16 Step   
*   1   |   0   |   1    |   1/32 Step
---------------------------------------
*
*  FUNCTION   |   STM32 Pin      DRV8825 Pin   |        Description
*     Step    |     PA8 ---------- 22-STEP     |  Steps motor 1.8 degrees(Full step) in set direction
*  Direction  |     PB12 --------- 20-DIR      |  Changes direction of motor, cw or ccw
*    Mode 0   |     PB15 --------- 24-M0       |  Used to change Microstepping index
*    Mode 1   |     PB14 --------- 25-M1       |  Used to change Microstepping Index
*    Mode 2   |     PB13 --------- 26-M2       |  Used to change Microstepping Index
*    Enable   |     PA9 ---------- 21-!EN      |  Enabled by low (0) / Disabled by high (1)
*********************************************************************************************************
*/
#include "utility.h"

#ifndef STEPCTRL_H_
#define STEPCTRL_H_

#ifdef __cplusplus
extern "C" { // link CPP files
#endif

class Stepper{
    
    public:
        Stepper();
        void setHome();
        void returnToHome();
        void setMode(uint8_t);
        void setPosition(float angle);
        void setDirection(bool);
        float getPosition();
        int getDivisor();
        void enable(bool);
        void disable(bool);
    private:
        float divisor;
        int stepResolution;
        float angle;
        int maxSpeed;
        int accelerationRate;
        int accelerate();
        int calculateSteps(float angle);
        
};


#ifdef __cplusplus
}
#endif



#endif
