
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
<<<<<<< HEAD
#include "mag_encoder.h"
=======
#include "stm32f1xx_it.h"
>>>>>>> 7213dad5ec7124301ffa63520b2de9aa2631a53e



/* Private Variables-----------------------------------------------------------*/
UART_HandleTypeDef huart1;	 			// interrupt handler
<<<<<<< HEAD
SPI_HandleTypeDef hspi1;
const uint8_t BUFFER_SIZE = 1;		// Size of Buffer
uint8_t bufferRX[BUFFER_SIZE];		   			// receives protocol
uint8_t bufferTX[BUFFER_SIZE]; 	// ping packet
Queue commandPackets(200);
const int ID = 2;
=======
const int BUFFER_SIZE = 14;		// Size of Buffer
const int BAUD_RATE = 57600;
const int ID = 1;
uint8_t bufferRX;
Queue commandPackets(200);

>>>>>>> 7213dad5ec7124301ffa63520b2de9aa2631a53e

/* Objects --------------------------------------------------------------------*/
Stepper stepper = Stepper(ID);
Queue buffer_queue = Queue(200); // queue that holds 200 characters
<<<<<<< HEAD
PacketHandler packet = PacketHandler(ID, 1000000, &stepper);
=======
PacketHandler packet = PacketHandler(ID, BAUD_RATE, &stepper);
>>>>>>> 7213dad5ec7124301ffa63520b2de9aa2631a53e



float true_angle = 0.0f;

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void) {
	
	initialSetup();
	stepper.setMode();
	
<<<<<<< HEAD
	uint8_t tx = 0xff;

	
	while(1) {
			
		//packet.readPacket();
		stepper.setPosition(50);
		HAL_Delay(1000);
		stepper.setPosition(1024);
		HAL_Delay(1000);
		
		
=======
	while(1) {
		stepper.goToTarget();
		packet.readPacket();
>>>>>>> 7213dad5ec7124301ffa63520b2de9aa2631a53e
	}
 

	return 0;
}
