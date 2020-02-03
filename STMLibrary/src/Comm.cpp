// // Converts serial com packets to understandable format.

#include "Comm.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* External Variables --------------------------------------------------------- */
extern Queue commandPackets;

/* Constant Variables --------------------------------------------------------- */

#define TXPACKET_MAX_LEN (1 * 1024)
#define RXPACKET_MAX_LEN (1 * 1024)
#define PACKET_MIN_LEN   11

/* Packet structure ----------------------------------------------------------- */

#define PKT_HEADER0 	0
#define PKT_HEADER1 	1
#define PKT_HEADER2 	2
#define PKT_RESERVED 	3
#define PKT_ID 			4
#define PKT_LENGTH_L 	5
#define PKT_LENGTH_H 	6
#define PKT_INSTRUCTION 7	
#define PKT_ERROR 		8
#define PKT_PARAMETER0 	8

/* Instruction Types ----------------------------------------------------------- */

#define INSTR_PING   0x01
#define INSTR_READ   0x02
#define INSTR_WRITE  0x03
#define INSTR_REGWR  0x04
#define INSTR_ACTION 0x05
#define INSTR_FCTRY  0x06
#define INSTR_REBOOT 0x08
#define INSTR_CLEAR  0x10
#define INSTR_STATUS 0x55
#define INSTR_SYNCRD 0x82
#define INSTR_SYNCWR 0x83
#define INSTR_BULKRD 0x92
#define INSTR_BULKWR 0x93

// Error Bits ---------------------

#define ERRNUM_RESULT_FAIL 1  // Failed to process the instruction packet.
#define ERRNUM_INSTRUCTION 2  // Instruction error
#define ERRNUM_CRC         3  // CRC check error
#define ERRNUM_DATA_RANGE  4  // Data range error
#define ERRNUM_DATA_LENGTH 5  // Data length error
#define ERRNUM_DATA_LIMIT  6  // Data limit error
#define ERRNUM_ACCESS      7  // Access error


/* Packet Handler -------------------------------------------------------------- */

// // variable packet length variable
PacketHandler::PacketHandler(Queue * buffer_queue) {
	packet_queue = buffer_queue;
}

PacketHandler::~PacketHandler() {}

/*
bool PacketHandler::readPacket() {
	packet = queue->deQueue();

	while (true) {
		uint16_t idx = 0;
		for (idx = 0; idx < (PACKET_MIN_LEN-3); idx++) {
			if ((packet[idx] == 0xFF) && (packet[idx + 1] == 0xFF) && 
				 (packet[idx+2] == 0xFD) && (packet[idx + 3] != 0xFD))
				break;
		}
		if (packet[idx+4] == STEP_ID) { // check if packet belongs to this stepper
		}


	}
}

*/

bool PacketHandler::readPacket(){
	uint8_t *currentCommand;
	currentCommand = commandPackets.deQueue(); // pull a command from queue

	/*
		currentCommand points to the next command packet ready
		to be deciphered.
	*/
	int i;
	uint8_t display_temp;
	for(i = 0; i < 24; i++){
		display_temp = currentCommand[i];
	}
	return true;
}




/* Circular Queue --------------------------------------------------------------*/

Queue::Queue() {
	rear = front = -1;
	queueSize = 10;
	packetSize = 24;
}


void Queue::enQueue(uint8_t *packetRX){

	if( (front == 0 && rear == queueSize-1) || (rear == (front-1)%(queueSize-1)) ){
		return; // error, queue is full
	} else if (front == -1) { // insert first element
		front = rear = 0;
	} else if (rear == queueSize-1 && front != 0) {
		rear = 0;
	} else {
		rear++;
	}

	loadArray(rear, packetRX);
}

void Queue::loadArray(int element, uint8_t *packetRX) {
	for(int i = 0; i < sizeof(arr[element]); i++) {
		arr[element][i]=packetRX[i];
	}
}

uint8_t* Queue::deQueue(){
	if (front == -1) return NULL; // error queue is empty
	
	int temp;
	temp = front;
	
	if (front == rear) {
		front = rear = -1;
	} else if (front == queueSize-1) {
		front = 0;
	}	else {
		front++;
	}

	return arr[temp];
}

