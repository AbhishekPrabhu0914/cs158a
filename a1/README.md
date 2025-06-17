Run With Short:

Server:
python myvlserver.py
Server is ready to receive...
Connected from 127.0.0.1
hello                                                        .
Length of Message Sent: 64
Connection closed
########################
Client
python3 myvlclient.py
Input lowercase sentence: 05hello
From Server: HELLO      

Run With Long:
Server:
Server is ready to receive...
Connected from 127.0.0.1
this_message_has_more_than_sixty_four_characters_and_it_is_val #This line shows that it was only accepted in bufsize blocks
processed: this_message_has_more_than_sixty_four_characters_and_it_is_valid_input!!                                                      
Length of Message Sent: 128
Connection closed

Client
python3 myvlclient.py
Input lowercase sentence: 70this_message_has_more_than_sixty_four_characters_and_it_is_valid_input!!
From Server: THIS_MESSAGE_HAS_MORE_THAN_SIXTY_FOUR_CHARACTERS_AND_IT_IS_VALID_INPUT!! 

