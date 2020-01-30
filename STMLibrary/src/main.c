
/**
******************************************************************************
* @file           : main.c
* @brief          : main.c file.
*                   This file serves as the entry point for the firmware which
*                   will be used to drive the stepper controller. The Micro-
*                   controller used is the STM32F103C8T6 or commonly known as 
*                   the bluepill.
* @date           : 1/29/2020
* @authors        : J. Brandon Iams
******************************************************************************
*/


/* Includes--------------------------------------------------------------------*/
#include "utility.h"
#include "StepCtrl.h"

/* Private Variables-----------------------------------------------------------*/
UART_HandleTypeDef huart1;



/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
	initialSetup();

  while (1)
  { 
		HAL_GPIO_WritePin(GPIOA, LED, GPIO_PIN_SET);
    HAL_Delay(1000);
		HAL_GPIO_WritePin(GPIOA, LED, GPIO_PIN_RESET);
		HAL_Delay(1000);
		
	}

}
