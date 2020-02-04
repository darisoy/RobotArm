// /*****
// EE475
// *****/

#ifndef COMM_H_
#define COMM_H_

#include <stdint.h>

/* instructions to receive
Ping packet
|  H1  |  H2   | H3  |	RSRV |  ID  | LEN1 | LEN2 | INST | CRC1 | CRC2
| 0xFF | 0xFF | 0xFD |	0x00 | 0xFE | 0x03 |	0x00 | 0x01 | 0x31 | 0x42

Write packet Example:
Write 512(0x00000200) to Goal Position(116, 0x0074, 4[byte])

|  H1	 |  H2  |  H3	| RSRV |  ID  | LEN1 | LEN2 | INST |  P1	|  P2	 |  P3  |  P4  |  P5	 | P6   | CRC1 | CRC2 |
| 0xFF |	0xFF | 0xFD	| 0x00 | 0x01 | 0x09 | 0x00 | 0x03 | 0x74 | 0x00 |	0x00 | 0x02 | 0x00 | 0x00 | 0xCA | 0x89 |


// Set Baud Rate

Set ID

Set Torque


In the future: read position

*/

/* Constant Variables --------------------------------------------------------- */

#define TXPACKET_MAX_LEN (1 * 1024)
#define RXPACKET_MAX_LEN (1 * 1024)
#define PACKET_MIN_LEN   11

/* Packet structure ----------------------------------------------------------- */

#define PKT_HEAD0 	0
#define PKT_HEAD1 	1
#define PKT_HEAD2 	2
#define PKT_RSVED 	3
#define PKT_ID 		4
#define PKT_LENL 	   5
#define PKT_LENH 	   6
#define PKT_INSTR    7	
#define PKT_ERROR 	8
#define PKT_PRAM0 	8

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



typedef struct Queue {
	
	/* variables */
	int rear, front, queueSize;
	// circular queue is 2D array where it contains up to 
	// 10 message of 24 bytes
	uint8_t *arr;
	Queue(uint16_t size){
		queueSize = size;
		arr = new uint8_t[size];
		rear = front = -1;
	}
	
	/* functions */
	void enQueue(uint8_t *packetRX);
	void loadArray(int element, uint8_t *packetRX);
	uint8_t* deQueue();
	
} Queue;


class PacketHandler {
	
	public:
		PacketHandler(Queue *);
		~PacketHandler(void);
		bool readPacket();
		char * getRxType(uint8_t *);
		char * getRxContent(uint8_t *);
		// send status type back to Pi
		char * sendStatus(uint8_t * status_type, uint8_t * status_packet);

	private:
		Queue * packet_queue;
		uint8_t* packet;
};

#endif

