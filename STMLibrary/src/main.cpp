
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
const int ID = 1;

/* Objects --------------------------------------------------------------------*/
Stepper stepper = Stepper(ID);
Queue buffer_queue = Queue(200); // queue that holds 200 characters
PacketHandler packet = PacketHandler(ID, 57600, &stepper);


/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void) {
	
	initialSetup();
	DWT_Init();
	HAL_Delay(100);
	stepper.setMode();
	
	while(1) {
		
		//stepper.setPosition(100);
		
		//LED PIN TOGGLE
		//HAL_GPIO_TogglePin(LED_Port, LED);
		//HAL_Delay(100);
		
		//STEPPER TESET
		
		//HAL_Delay(1000);
		//stepper.setPosition(200);
		//HAL_Delay(1000);
		
		packet.readPacket();
		
	}
 

	return 0;
}
