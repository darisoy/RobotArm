
//EEPROM AREA
#define	MODEL_NUMBER         0           
#define	MODEL_INFORMATION    2                
#define	FIRMWARE_VERSION     6               
#define	ID                   7 
#define	BAUD_RATE            8        
#define	RETURN_DELAY_TIME	 9                   
#define	DRIVE_MODE           10         
#define	OPERATING_MODE	 	 11                  
#define	SECONDARY_ID         12           
#define	PROTOCOL_TYPE        13            
#define	HOMING_OFFSET        20            
#define	MOVING_THRESHOLD     24               
#define	TEMPERATURE_LIMIY    31                
#define	MAX_VOLTAGE_LIMIT    32                
#define	MIN_VOLTAGE_LIMIT	 34                   
#define	PWM_LIMIT            36        
#define	VELOCITY_LIMIT       44             
#define	MAX_POSITION_LIMIT   48                 
#define	MIN_POSITION_LIMIT 	 52                  
#define	SHUTDOWN             63 

//CONTROL TABLE
#define	TORQUE_ENABLE          64            
#define	LED                    65  
#define	STATUS_RETURN_LEVEL    68                  
#define	REGISTERED_INSTRUCTION 69                     
#define	HARDWARE_ERROR_STATUS  70                    
#define	VELOCITY_I_GAIN        76              
#define	VELOCITY_P_GAIN        78              
#define	POSITION_D_GAIN        80              
#define	POSITION_I_GAIN        82              
#define	POSITION_P_GAIN        84              
#define	FEEDFORWARD_2ND_GAIN   88                   
#define	FEEDFORWARD_1ST_GAIN   90                   
#define	BUS_WATCHDOG           98           
#define	GOAL_PWM               100       
#define	GOAL_VELOCITY          104            
#define	PROFILE_ACCELERATION   108                   
#define	PROFILE_VELOCITY       112               
#define	GOAL_POSITION          116            
#define	REALTIME_TICK          120            
#define	MOVING                 122     
#define	MOVING_STATUS          123            
#define	PRESENT_PWM            124          
#define	PRESENT_LOAD           126           
#define	PRESENT_VELOCITY       128               
#define	PRESENT_POSITION       132               
#define	VELOCITY_TRAJECTORY    136                  
#define	POSITION_TRAJECTORY    140                  
#define	PRESENT_INPUT_VOLTAGE  144                    
#define	PRESENT_TEMPERATURE    146                  