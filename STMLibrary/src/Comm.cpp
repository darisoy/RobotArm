// // Converts serial com packets to understandable format.

#include "Comm.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* External Variables --------------------------------------------------------- */
extern Queue commandPackets;


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

// bool PacketHandler::readPacket(){
// 	uint8_t *currentCommand;
// 	currentCommand = commandPackets.deQueue(); // pull a command from queue

// 	/*
// 		currentCommand points to the next command packet ready
// 		to be deciphered.
// 	*/
// 	int i;
// 	uint8_t display_temp;
// 	for(i = 0; i < 24; i++){
// 		display_temp = currentCommand[i];
// 	}
// 	return true;
// }

bool PacketHandler::readPacket(){
	uint8_t *current_packet;
	current_packet = commandPackets.deQueue(); // pull a command from queue

	/*
		currentCommand points to the next command packet ready
		to be deciphered.
	*/
	int i;
	uint8_t display_temp;
	for(i = 0; i < 24; i++) {
		display_temp = current_packet[i];
	}
	
	uint8_t * packet_data = commandPackets.deQueue();
	while ((*packet_data != 0xFF) && (*packet_data != NULL)) packet_data = commandPackets.deQueue();
	
	for (i = 0; i < 24 - 3; i++) {
		if ((current_packet[i] == 0xFF) && 
			  (current_packet[i+1] == 0xFF) && 
				(current_packet[i+2] == 0xFD) && 
		    (current_packet[i+3] != 0xFD))
			break;
		if (i == 20) i = -1;
 	}
	
	int data_len;
	if ((current_packet[i+4] == STEP_ID) && (i != -1)) { // data exists
		data_len = (current_packet[i+PKT_LENL]-'0') + 10*(current_packet[i+PKT_LENH]-'0');
	}
	
	int instr_type;
	instr_type = current_packet[i+PKT_INSTR];
	switch(instr_type) {
		case INSTR_PING:
			// if stm status is good, send ping back.
			// uint8_t return_packet[11] = {0xFF, 0xFF, 0xFD, 0x00, STEP_ID, }; 
			// 'ff:ff:fd:0:4:4:0:55:80:3a:8e'
			break;
		case INSTR_READ:
			break;
		case INSTR_WRITE:
			break;
		case INSTR_REGWR:
			break;
		case INSTR_ACTION:
			break;
		case INSTR_FCTRY:
			break;
		case INSTR_REBOOT:
			break;
		case INSTR_CLEAR:
			break;
		case INSTR_STATUS:
			break;
		case INSTR_SYNCRD:
			break;
		case INSTR_SYNCWR:
			break;
		case INSTR_BULKRD:
			break;
		case INSTR_BULKWR:
			break;
	}
} 



/* Circular Queue --------------------------------------------------------------*/

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

