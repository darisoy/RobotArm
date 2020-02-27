
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
#include <stdio.h>
#include <string.h>
#include "utility.h"
#include "StepCtrl.h"
#include "Comm.h"



/* Private Variables-----------------------------------------------------------*/
UART_HandleTypeDef huart1;	 			// interrupt handler
const uint8_t BUFFER_SIZE = 24;		// Size of Buffer
uint8_t bufferRX[BUFFER_SIZE];		   			// receives protocol
uint8_t bufferTX[BUFFER_SIZE]={0xFF, 0xFF, 0xFD, 0x00, 0xFE, 0x03, 0x00, 0x01, 0x31, 0x42}; // ping packet
Queue commandPackets;



/* Objects --------------------------------------------------------------------*/
Stepper stepper = Stepper();
PacketHandler packet = PacketHandler();


/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

	initialSetup();
	//HAL_Delay(100);	
	//HAL_UART_Transmit_IT(&huart1, bufferTX, sizeof(bufferTX));
	HAL_Delay(100);

  while (1)
  { 
		HAL_GPIO_TogglePin(LED_Port, LED);
		HAL_Delay(1000);
		//HAL_Delay(500);
		//packet.readPacket();
	}
	return 0;
}
