
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

/* Circular Queue --------------------------------------------------------------*/
struct Queue{
	// initialize front and rear
	int rear, front;
	
	// circular queue
	int size;
	uint8_t *arr;
	
	Queue(int size){
		front = rear = -1;
		arr = new uint8_t [size];
	}
	void enQueue(uint8_t &packet_rx);
	uint8_t* deQueue();
};

void Queue::enQueue(uint8_t &packet_rx){
	if( (front == 0 && rear == size-1) || (rear == (front-1)%(size-1)) ){
		// error, queue is full
		return;
	} else if (front == -1) { // insert first element
		front = rear = 0;
		arr[rear] = packet_rx;
	} else if (rear == size-1 && front != 0) {
		rear = 0;
		arr[rear] = packet_rx;
	} else {
		rear++;
		arr[rear] = packet_rx;
	}
}

uint8_t* Queue::deQueue(){
	if (front == -1) {
		// error queue is empty
		return NULL;
	} 
	uint8_t* top_packet = &arr[front];
	arr[front] = NULL;
	if (front == rear) {
		front = -1;
		rear = -1;
	} else if (front == size-1) {
		front = 0;
	}	else {
		front++;
	}
	return top_packet;
}

/* Private Variables-----------------------------------------------------------*/
UART_HandleTypeDef huart1;	 			// interrupt handler
const uint8_t BUFFER_SIZE = 20;		// Size of Buffer
uint8_t buffer_rx[BUFFER_SIZE];		   			// receives protocol
uint8_t buffer_tx[BUFFER_SIZE];			 			// transmits reply

Queue command_packets(10);
	
// TESTING VARIABLE, DELETE LATER
bool DIRECTION = false;

/* Objects --------------------------------------------------------------------*/
Stepper stepper = Stepper();

/* Interrupt Service Routine---------------------------------------------------*/
/*
void USART1_IRQHandler(void){
	HAL_UART_IRQHandler(&huart1);
	HAL_UART_Receive_IT(&huart1, buffer_rx, sizeof(buffer_rx));
	
}
*/
void MX_USART1_UART_Init(void);
	
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){
	// Receive UART1 data in interrupt mode
	//HAL_UART_Receive_IT(&huart1, buffer_rx, sizeof(buffer_rx));
	//command_packets.enQueue(*buffer_rx);
	__NOP();
}


/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
	initialSetup();
	stepper.setMode(1);
	HAL_Delay(1000);	
	MX_USART1_UART_Init();
	HAL_UART_Receive_IT(&huart1, buffer_rx, sizeof(buffer_rx));
	
	
  while (1)
  { 
		DIRECTION = !DIRECTION;  
		stepper.setPosition(90);
		HAL_Delay(500);
		stepper.setDirection(DIRECTION);
		//HAL_UART_Receive(&huart1, buffer_rx, sizeof(buffer_rx), 2000);
	}

}


/**
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */
void MX_USART1_UART_Init(void)
{
	//UART_HandleTypeDef huart1;

  /**USART2 GPIO Configuration
  PB6     ------> USART2_TX
  PB7     ------> USART2_RX
  */
	
  /*  USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 57600;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
	//HAL_NVIC_SetPriority(USART1_IRQn, 0, 0);
	//HAL_NVIC_EnableIRQ(USART1_IRQn);

}