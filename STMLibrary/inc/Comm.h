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

Set Torque


In the future: read position

*/

struct Queue {
	// variables
	int rear, front; // front & rear pointers
	int size; // size of queue
	uint8_t *arr;
	// functions
	Queue(int);
	void enQueue(uint8_t &packet_rx);
	uint8_t* deQueue();
};


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
	Queue * queue;
	uint8_t* packet;
};

// class PortHandler {
// public:
// 	// HAL_UART_Transmit()
// 	// HAL_UART_Receive()
// private:
// };

#endif