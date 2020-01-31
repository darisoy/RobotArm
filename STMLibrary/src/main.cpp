
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

/* Objects --------------------------------------------------------------------*/



void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart){
	
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){
	while(1);
}


/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
	initialSetup();
	HAL_Delay(1000);
	uint8_t buffer_tx[10]={'a','a','a','a','a','a','a','a','a'};
	uint8_t buffer_rx[1];
	
	//HAL_UART_Receive_IT(&huart1, buffer_rx, sizeof(buffer_rx));
	//HAL_UART_Transmit_IT(&huart1, buffer_tx, sizeof(buffer_tx));
	
	
  while (1)
  { 
		HAL_UART_Receive(&huart1, buffer_rx, sizeof(buffer_rx), HAL_MAX_DELAY);
		HAL_Delay(100);
		//if(buffer[0]=='a'){
		//	HAL_GPIO_WritePin(LED_Port, LED, GPIO_PIN_SET);
		//}
	}

}
