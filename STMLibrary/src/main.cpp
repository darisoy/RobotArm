
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
#include "dwt_delay.h"
#include "utility.h"
#include "StepCtrl.h"
#include "Comm.h"



/* Private Variables-----------------------------------------------------------*/
UART_HandleTypeDef huart1;	 			// interrupt handler
const uint8_t BUFFER_SIZE = 1;		// Size of Buffer
uint8_t bufferRX[BUFFER_SIZE];		   			// receives protocol
uint8_t bufferTX[BUFFER_SIZE]; 	// ping packet
Queue commandPackets(200);


/* Objects --------------------------------------------------------------------*/
Stepper stepper = Stepper(1);
Queue buffer_queue = Queue(200); // queue that holds 200 characters
PacketHandler packet = PacketHandler(1, 57600);

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void) {

	initialSetup();
	
	stepper.setMode();
	stepper.setPosition(1991);
	HAL_Delay(2000);
	
  while (1) { 
	
		packet.readPacket();
		HAL_Delay(2000); 
		
	}
	return 0;
}
