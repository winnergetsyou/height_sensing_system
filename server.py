#!/usr/bin/python3
#----------------------------------------------------------------------------------
# INCLUDING ALL ESSENTIAL HEADER FILES FOR SOCKET PROGRAMMING
#----------------------------------------------------------------------------------
import socket
import sys
from struct import *
# height is a seperately created python class which converts raw laser input to height in cms .This can be used with other sensor raw values as well with little modification.
from height import Height
#----------------------------------------------------------------------------------
#socket_programming_part
#----------------------------------------------------------------------------------

HOST = ''	
PORT = 12778	

# CREATING SOCKET WITH IPV4 [AF_INET] AND UDP datagrams [socket.SOCK_DGRAM]
so= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('Socket created')

# BINDING SOCKET TO THE PORT -12778
so.bind((HOST, PORT))
print('Socket bind complete')

#-----------------------------------------------------------------------------------
#port_details for sending HEIGHTs in cm
udp_host = socket.gethostname()	
udp_port = 12777
# 12777 - message_router
#------------------------------------------------------------------------------------

#####################################################################################
# HSS variables
#-----------------------------------------------------------------------------------

laser_head = 43521    #AA01
engine_head = 43537   #AA11
height_head = 43569   #AA31
elapsed = 0
H=0                   #HEIGHT
M=[]                  #UNPACKING
#packed_msg
#packed_msg_TWO
#-----------------------------------------------------------------------------------
# ALGORITHM
#-----------------------------------------------------------------------------------
## listens for data !
while 1:
	data = so.recvfrom(4096)
	message = data[0]
	address = data[1]
	
	######------------algorithm to find the _field_header from the udp_messages----##############
	z=bin(int.from_bytes(message, byteorder=sys.byteorder))  # => gives binary something like '0b10001'
	l=len(z)
	a=z[l-8:l]
	b=z[l-16:l-8]
	c=str(a)+str(b)
	d=int(c,2)
	print(d)
	#print('jjjjjj')
	#######------------------------------------------------------------------------###############
	
	
	if(d==laser_head):
	
		##1. UNPACKING
		M=unpack('!HLHHH',message)
		print([M[0]])
		elapsed = M[1]
		
		##2. finding height in cms USING THE IMPORTED CLASS(THIS CLASS HAS BEEN CREATED SEPERATELY FOR REUSE) 
		Object=Height
		H = Object.height(M[2],M[3],M[4])
		H = int(H)
		
		##3. PACKING and SENDING
	
		packed_msg=pack('!HLL',height_head,elapsed,H)
		#print(packed_msg)
		#print(calcsize('!HLL'))
		#print(unpack('!HLL',packed_data))

		## SENDING TO MESSAGE ROUTER 12777
		so.sendto(packed_msg,(udp_host,udp_port))
		print("Height_msg_send_to_al_sub_systems_in_cms")
		
				
		## assuming LANDING at 40cm ! SINCE HEIGHT OF SPACE-CRAFT After landing 40 cm! Landing detected ## WE CAN USE OTHER SIGNALS AS WELL IN THE PLACE OF 40 CM .
		if(H <= 40): 
			#PACKING-- ENGINE_CUTOFF-->Engine_head
			packed_msg_TWO=pack('!HL',height_head,engine_head)
			#SENDING
			so.sendto(packed_msg,(udp_host,udp_port))
			#print("I came upto here")
#CLOSING THE SOCKET(if comes out of while)...
so.close()
			

