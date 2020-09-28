# wiredworks_winches

#Branch v.0.0.3 is ready to be experimented with!

At this stage you can create multiple nodes which, by pushing the start button,
call an operator which set a USocket connection at a specific IP:Port combination up.

By checking the left check-box the data transfer starts unticking this box stopps the 
transfer. The right checkbox indicates that the transfer is started (never trust that
a command does as expected). Opening a USocket with the same IP:port combination shows
a dialog box and you can enter a different adress.

Deleting the node will delete the USockets - a Key error will be thrown not a bad thing
as the operator is destroyed I still have to find a better way to do this.

To Try the add-on:

go to the UClients_and_helpers dir and start the three clients

get the wiredworks_winches dir into the addons dir of Blender

Start Blender

Load it with the preferences Menue

doublicate the Cube 2 times so that you hve Cube, Cube.001 and Cube.002

open a node editor choose ww_SFX_Nodes

add a new tree

add a new node

set the adress to 127.0.0.1, the recPort (left field) to 15021 and the sendPort (right field) to 15022

push the start button

tick the left checkbox

--> the communication with the first Client should be started

ad another node

set the adress to 127.0.0.1, the recPort (left field) to 15023 and the sendPort (right field) to 15024

push the start button

tick the left checkbox

--> the communication with the second Client should be started

ad another node

set the adress to 127.0.0.1, the recPort (left field) to 15025 and the sendPort (right field) to 15026

push the start button

tick the left checkbox

--> the communication with the first Client should be started

moving the Joystick will move the Cubes.

Known Problems:

  Key error when destroying an Actuator Node
  
  each operator starts a timer so the frequency of the communication is dependent on the number of nodes
  
  # After Restructuring
  
  got rid of Key error when destroying an Actuator node
  
  only one timer running
  
  once the communication with the Actuators has started it seems to be stable
  
  # But
  
  During registering of the Actuators sometimes strange behavior can be observed
  
  especially when trying to register an actuator to an already opened USocket.
  
  MOre experiments are needed. But my knowledge of the internals of Blender are limited
  




