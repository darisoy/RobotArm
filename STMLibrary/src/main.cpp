
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
#include "stm32f1xx_it.h"



/* Private Variables-----------------------------------------------------------*/
UART_HandleTypeDef huart1;	 			// interrupt handler
const int BUFFER_SIZE = 14;		// Size of Buffer
const int BAUD_RATE = 57600;
const int ID = 1;
uint8_t bufferRX;
Queue commandPackets(200);


/* Objects --------------------------------------------------------------------*/
Stepper stepper = Stepper(ID);
Queue buffer_queue = Queue(200); // queue that holds 200 characters
PacketHandler packet = PacketHandler(ID, BAUD_RATE, &stepper);


/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void) {
	
	initialSetup();
	stepper.setMode();
	
	while(1) {
		stepper.goToTarget();
		packet.readPacket();
	}
 

	return 0;
}
