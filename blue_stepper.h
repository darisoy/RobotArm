/* Author(s): J. Brandon Iams
 *
 * Date  : 1/16/2020
 * File  : stepper.h
 * Desc  : Controls stepper motors through stepper driver DRV8825.
 *
 */ 

#ifndef __blue_stepper_H__
#define __blue_stepper_H__

#include <stdio.h>
#include <stdint.h>

class BlueStepper{
    public:
        BlueStepper();
        void setHome();
        void returnToHome();
        void setMode(int m2, int m1, int m0);
        void setPosition(float angle);
        float getPosition();
        int getDivisor();
        void enable(bool);
        void disable(bool);
    private:
        int DIR;
        int STEP;
        int M2;
        int M1;
        int M0;
        int EN;
        float divisor;
        int stepResolution;
        float angle;
        int delay;
        void calculateDivisor();
        int calculateSteps(float angle);
};

#endif
