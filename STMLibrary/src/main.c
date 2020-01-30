/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */

#include "utility.h"

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
