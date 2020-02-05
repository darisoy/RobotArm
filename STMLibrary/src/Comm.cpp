// // Converts serial com packets to understandable format.

#include "Comm.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* External Variables --------------------------------------------------------- */
extern Queue commandPackets;


/* Packet Handler -------------------------------------------------------------- */

// // variable packet length variable
PacketHandler::PacketHandler(uint8_t ID, uint32_t BAUD) {
	node.ID = ID;
	node.BAUD_RATE = BAUD;
}

PacketHandler::~PacketHandler() {}

bool PacketHandler::sendPacket(int size) {
	// HAL_UART_Transmit_IT(&huart1, bufferRX, sizeof(bufferRX));
}

uint64_t PacketHandler::executePacket(uint8_t inst, uint8_t len) {
	uint8_t tx_packet[20] = {0xFF, 0xFF, 0xFD, 0x00, node.ID};
	switch(inst) {
		case INSTR_PING  :
			//ping back
			tx_packet[PKT_LENL] = 0x07;
			tx_packet[PKT_LENH] = 0x00;
			tx_packet[PKT_INSTR] = INSTR_STATUS;
			tx_packet[PKT_ERROR] = 0x00;
			tx_packet[PKT_PARAM1] = 0x06; 
			tx_packet[PKT_PARAM2] = 0x04;
			tx_packet[PKT_PARAM3] = 0x26;
			updateCRC(0, tx_packet+12, 12);
			// tx_packet[12] = 0x00;
			// tx_packet[13] = 0x00;
			sendPacket(14);
		break;
		case INSTR_READ  :
			//send back data
			//read()
		break;
		case INSTR_WRITE :
		break;
		case INSTR_REGWR :
		break;
		case INSTR_ACTION:
		break;
		case INSTR_FCTRY :
		break;
		case INSTR_REBOOT:
		break;
		case INSTR_CLEAR :
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
		default:
			//do nothing
		
	}
}

bool PacketHandler::readPacket(){
	// int check_index = -1, data_length;
	// bool addr_check =  false;
	uint8_t instr_type, len, id;
	
	while(!commandPackets.isEmpty()){
		if(commandPackets.bytesUsed() < 10){
			continue;
		}
		if(commandPackets.peekBy(4) != 0xFFFFFD00){
			commandPackets.deQueue();
		}else{
			commandPackets.deQueue();
			commandPackets.deQueue();
			commandPackets.deQueue();
			commandPackets.deQueue();
			id = commandPackets.deQueue();
			len = commandPackets.deQueue() + (commandPackets.deQueue() << 8) - 3;
			instr_type = commandPackets.deQueue();
			for (int i = 0; i > len; i++){
				params[i] = commandPackets.deQueue();
			}
			commandPackets.deQueue();
			commandPackets.deQueue();
			if(id == node.ID){
				executePacket(instr_type,len);
			}
		}
	}

	// while(commandPackets.peek() != 0xFF && !commandPackets.isEmpty()) {
	// 	commandPackets.deQueue();
	// }
	// check_index = -1;
	//
	// while(!commandPackets.isEmpty()) {
	// 	uint8_t cur_val = commandPackets.peek();
	// 	switch(check_index) {
	// 		case -1:
	// 			if (cur_val == 0xFF) check_index++;
	// 			break;
	// 		case 0:
	// 			check_index = (cur_val == 0xFF) ? check_index + 1 : -1;
	// 			break;
	// 		case 1:
	// 			check_index = (cur_val == 0xFD) ? check_index + 1 : -1;
	// 			break;
	// 		case 2:
	// 			check_index = (cur_val == 0x00) ? check_index + 1 : -1;
	// 			// make sure it's not FD because that means there is an error
	// 			break;
	// 		case 3:
	// 			check_index++;
	// 			addr_check = (cur_val == STEP_ID) ? true : false;
	// 			break;
	// 		case 4:
	// 			check_index++;
	// 			data_length = cur_val - '0';
	// 			break;
	// 		case 5:
	// 			check_index++;
	// 			data_length += 8 << (cur_val - '0');
	// 			break;
	// 		case 6:
	// 			check_index++;

	// 			break;
	// 	}
	// }
	
	// if(!commandPackets.isEmpty()){
	// 	//commannPackets.lookAt[
	// 	h1 = commandPackets.deQueue(); // pull a command from queue
	// 	h2 = commandPackets.deQueue(); 
	// 	h3 = commandPackets.deQueue(); 
	// 	if(commandPackets.peek() == 0xff){
	// 		h1 = commandPackets.deQueue();
	// 		if(commandPackets.deQueue() == 0xff){
	// 			if(commandPackets.deQueue() == 0xfd){
	// 				commandPackets.deQueue(); //pop out RSRV byte
	// 				if(commandPackets.deQueue()==node.ID){
	// 					commandPackets.deQueue(); //pop out LEN1 byte
	// 					commandPackets.deQueue(); //pop out LEN2 byte
	// 					this->instruction = commandPackets.deQueue(); //pop out instruction byte
	// 				}
	// 			}
	// 		}
	// 	}
	// }





	return true;
}

unsigned short PacketHandler::updateCRC(uint16_t crc_accum, uint8_t *data_blk_ptr, uint16_t data_blk_size) {
	uint16_t i;
	static const uint16_t crc_table[256] = {0x0000,
	0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
	0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027,
	0x0022, 0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D,
	0x8077, 0x0072, 0x0050, 0x8055, 0x805F, 0x005A, 0x804B,
	0x004E, 0x0044, 0x8041, 0x80C3, 0x00C6, 0x00CC, 0x80C9,
	0x00D8, 0x80DD, 0x80D7, 0x00D2, 0x00F0, 0x80F5, 0x80FF,
	0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1, 0x00A0, 0x80A5,
	0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1, 0x8093,
	0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
	0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197,
	0x0192, 0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE,
	0x01A4, 0x81A1, 0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB,
	0x01FE, 0x01F4, 0x81F1, 0x81D3, 0x01D6, 0x01DC, 0x81D9,
	0x01C8, 0x81CD, 0x81C7, 0x01C2, 0x0140, 0x8145, 0x814F,
	0x014A, 0x815B, 0x015E, 0x0154, 0x8151, 0x8173, 0x0176,
	0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162, 0x8123,
	0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
	0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104,
	0x8101, 0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D,
	0x8317, 0x0312, 0x0330, 0x8335, 0x833F, 0x033A, 0x832B,
	0x032E, 0x0324, 0x8321, 0x0360, 0x8365, 0x836F, 0x036A,
	0x837B, 0x037E, 0x0374, 0x8371, 0x8353, 0x0356, 0x035C,
	0x8359, 0x0348, 0x834D, 0x8347, 0x0342, 0x03C0, 0x83C5,
	0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1, 0x83F3,
	0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
	0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7,
	0x03B2, 0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E,
	0x0384, 0x8381, 0x0280, 0x8285, 0x828F, 0x028A, 0x829B,
	0x029E, 0x0294, 0x8291, 0x82B3, 0x02B6, 0x02BC, 0x82B9,
	0x02A8, 0x82AD, 0x82A7, 0x02A2, 0x82E3, 0x02E6, 0x02EC,
	0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2, 0x02D0, 0x82D5,
	0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1, 0x8243,
	0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
	0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264,
	0x8261, 0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E,
	0x0234, 0x8231, 0x8213, 0x0216, 0x021C, 0x8219, 0x0208,
	0x820D, 0x8207, 0x0202 };

	for (uint16_t j = 0; j < data_blk_size; j++) {
		i = ((uint16_t)(crc_accum >> 8) ^ *data_blk_ptr++) & 0xFF;
		crc_accum = (crc_accum << 8) ^ crc_table[i];
	}

	return crc_accum;
}

/* Circular Queue --------------------------------------------------------------*/

void Queue::enQueue(uint8_t packetRX){

	if( (front == 0 && rear == queueSize-1) || (rear == (front-1)%(queueSize-1)) ){
		return; // error, queue is full
	} else if (front == -1) { // insert first element
		front = rear = 0;
	} else if (rear == queueSize-1 && front != 0) {
		rear = 0;
	} else {
		rear++;
	}
	arr[rear] = packetRX;
}


uint8_t Queue::deQueue(){
	if (front == -1) return NULL; // error queue is empty
	
	uint8_t data = arr[front];
	//arr[front]=0x00;
	
	if (front == rear) {
		front = rear = -1;
	} else if (front == queueSize-1) {
		front = 0;
	}	else {
		front++;
	}

	return data;
}

uint8_t Queue::peek(){
	return peekAhead(0);
}

uint8_t Queue::peekAhead(int i ) {
	return *(arr + ((i + front) % queueSize));
}

bool Queue::isEmpty(){
	if(rear==front){
		return true;
	} else{
		return false;
	}

}

uint64_t Queue::peekBy(uint8_t val){
	if (val > 8){
		return -1;
	}
	int i;
	uint64_t message = 0 ;
	for(i=0; i<val; i++){
		message |= peekAhead(i) << i*8;
	}
	return message;
}

uint8_t Queue::bytesUsed(){
	return rear>front? rear-front : front + queueSize - rear
}
