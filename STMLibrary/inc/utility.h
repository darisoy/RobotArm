
/**
******************************************************************************
* @file           : utility.h
* @brief          : Header for main.c file.
*                   This file is responsibile for initializing the STM32 for 
*                   GPIO function, UART communicaiton, Timers, SPI Communication, 
*                   ADC temperature sensor, and PWM function.
* @date           : 1/29/2020
* @authors        : J. Brandon Iams
******************************************************************************
*/

#ifndef __UTILITY_H
#define __UTILITY_H

#ifdef __cplusplus
extern "C" { // link CPP files
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"
#include <stdint.h>

/* Private defines -----------------------------------------------------------*/
#define LED             GPIO_PIN_3
#define DIR             GPIO_PIN_12
#define M2              GPIO_PIN_13
#define M1              GPIO_PIN_14
#define M0              GPIO_PIN_15
#define STEP            GPIO_PIN_8
#define ENABLE          GPIO_PIN_9
#define DATA_DIR        GPIO_PIN_5

#define LED_Port        GPIOA
#define DIR_Port        GPIOB
#define M2_Port         GPIOB
#define M1_Port         GPIOB
#define M0_Port         GPIOB
#define STEP_Port       GPIOA
#define ENABLE_Port     GPIOA
#define DATA_DIR_Port   GPIOB


/* Function Wrappers----------------------------------------------------------*/
void digitalWrite(uint16_t pin, uint16_t state);
void delay(uint16_t);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);
void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Setup Block ---------------------------------------------------------------*/
void initialSetup(void);
void MX_GPIO_Init(void);
void SystemClock_Config(void);
void MX_SPI1_Init(void);
void MX_TIM2_Init(void);
//void MX_USART1_UART_Init(void);
void MX_ADC1_Init(void);



#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
