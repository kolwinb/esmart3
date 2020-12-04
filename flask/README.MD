# esmart3 rs485 communication protocol

## Modules

1. Python modules
 - api.py
   > properties and methods
 - settings.py
   > configuration of api
 - server.py
   > flask have been used



## About Hexdecimal

1. Recieved Code
	b'\xaa\x01\x01\x03\x00 \x00\x00\x00\x00\xfe\x04\x01\x01\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x1f\x00 \x00C\x00\x06\x00\xf8\xd4@\x00\x9b'

	> b'\0xfe\0x04'

2. 0xFE         	| 0x04
   -------------	|------------
   15	   14		| 0	4
   16^1   16^0		| 16^1 16^0
   15(16)  14(1) 	| 0(16) 4(1)
   240 + 14 =254	| 0+4=4
   1111 1110   		| 0000 0100
    254			| 4
   Change order min to max
    4			| 254
   convert 256 base number
   256^1  		| 256^0
   4(256) 		| 254(1)
    1024 		| 254
    1024+254
    1278 / 10.0
    127.8 V


3. Example Code
	- tem=''
	- a=ord(b'\xFE')                                                                                                
	- b=ord(b'\x04') 
        - print ("a={},b={}".format(a,b))                                                                               
        - if (a > b):                                                                                                   
        - temp=a
        - a=b
        - b=temp
        - print ("a={},b={}".format(a,b))
        - aa=a*256                                                                                                      
        - bb=b*1                                                                                                        
        - c=(aa+bb)/10.0
        - print ("c={} V".format(c)) 

4. OUTPUT

	- a=254,b=4
	- a=4,b=254
	- c=127.8 V

