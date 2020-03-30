The Test Cell Controller 

--> this is where the broker is running ... maybe it is best to pack all
the MQTT stuff (at least the server part) here under ?

--> also the client stuff can reside here under I would say :-)

the launching scripts for all elements should reside in ATE.scripts, as upon
install these become available to the OS.

Let yourself be inspired by the 'skeleton.py' file that resides there or not, 
BUT *OBSERVE* the shebang !!!
