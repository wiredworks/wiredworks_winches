

# Blender for SFX (MOCO) Stunts and Shows (How to)

![Screen](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Screen.png)



Blender is a very powerful tool to manipulate the virtual world of film and videos. It excels in the field of VFX whereas the field of SFX and the manipulation of the physical set is left to proprietary solutions.
Having such a solution designed, built, gotten the TÜV approval, it has been used on a number of A-movies. I would now like to invoke the Open Source approach that has Blender thriving, hoping other users are going to be as fascinated as I am myself in getting Blender to interact with the power SFX (MOCO) Stunts and Shows need.



## Installation:
Download Blender add-on from: https://github.com/wiredworks/wiredworks_winches
After getting the .zip remove '-master' from the filename and unzip it to the Blender scripts/add-ons folder. Take the modified Node Editor (/UClients_and_helpers/space-node.py and overwrite the standard Node Editor (/Programs/Blender Foundation/Blender 2.83/2.83/scripts/startup/bl_ui/space_node.py). Start Blender and activate the addon (Blender-> Edit-> Preferences-> Add-ons).

## New Example with Dana Dolly


![Joystick](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Dana_Dolly.png)

This Example shows a connection from the Joystick to Blender and from Blender to three Simulated Axes.

1.In UClients_and_helpers Start: 

-Dana_Dolly_Joystick.bat

-Dana_Dolly_Pan.bat

-Dana_Dolly_Tilt.bat

-Dana_Dolly_Track.bat


2.Start Blender install and activate addon

-Load danadolly.blend

-activate the checkboxes in the indicated sequence

3.Press Button6 on Gamepad and wiggle the Joystick to see the Dolly Tracking and the Head Pan- and Tilting 


### Example of all the basic Nodes.

To experiment with the example you have to have a Joystick/Gamepad and run Uclients_and_helpers/Joystick17.py this app takes Joystick-input displays it and sends it via UDP to the SFX-Nodes in Blender.

![Joystick](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Joystick17.png)

The simple_AxisSimulation.py script, once started will take UDP packages the SFX-Nodes emit and simulate a simple Axis/Actuator/Motor.

![simple](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/simple_AxisSimulation.png)


## Run the example

![Example](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Blender%20for%20SFX.png)


Start the external Programs ->

Start Blender ->

load Example1.blend ->

1.Push the Start Button -> 

2.check connect TickBox of the Joystick Node ->

![17](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Step1-2.png)

3.check connect TickBox of the Actuator Node  ->

4.Confirm Actuator Properties ->

![18](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Step3-4.png)

5.To Time in Cue Node ->

6.Confirm Cue ->

![19](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Step5-6.png)

Play with Joystick

 
 
 
 
 

# The Nodes:
There are:
Clocks, Sensors, Actuators, Cues, Helpers

## Clock:
Each Blender for SFX Node Tree has to have exactly one clock:

![1](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Clock.png)

that has to be started, by clicking the left checkbox, to execute the Tree.

![2](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Clock1.png)

The right checkbox is set when the Operator is running modal.

![3](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Clock2.png)


Each single Node has those checkboxes so that their execution can be controlled individually. The text field on the right is a sanity-check showing the 'TickTime' , the execution time, of the control loop so once the Tree is started the jitter of execution Time will be shown.
The clock also instantiates a Collection (ww SFX_Nodes) where the Actuators and Cues interact with the rest of Blender

## Sensors/Joystick:
	

The text fields: Name, IP-ADDRESS, RECEIVE-PORT, SEND-PORT of the socket

![4](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/JoystickA.png)


the other 	two checkboxes control the UDP-SOCKET. The same information is needed for the Actuator 	Node.


![5](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/JoystickB.png)

	
The normalized to 100 Joystick-input values can be viewed by enabling the respective box.

![6](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/JoystickC.png)
 
 
## Helpers / Demux:
	
 In this Node the Joystick-input signal is de-muxed, the Input is split into 3-channels, one 	float and two bools for the buttons.

![7](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Demux1.png)

Those Signals are selected by using the drop-down list
  
![8](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Demux2.png)
   
## Helpers / Mixer,Adder

These Nodes Mix or Add the Input Signal

![9](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Addern.png)

and the Expanded Basic Data

![10](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Adder1.png)

Shows the Data of the Actuator (not editable) 





## Actuators / LinRail

This Node interfaces the NodeTree to the Physical Motor using UDP-SOCKETS and instantiates some Objects in the ww SFX_Nodes collection and represents a slider/rail

![11](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/linrail.png)

 
The first line contains the same Information as in the Joystick Node (Name, Adress,...) the second Line of tick-boxes show the Status of the Actuator (Online,Enable,Selected) and if the data of the physical setup is confirmed.
In the Basic Data box: Set Velocity Actual Velocity, Actual Position, Enable, Select and Status.
The Digital Twin Data: Start of Rail, Position of the Connector (other Objects will be parented to this), End of Rail, Length, Moment of Inertia.
The Simple Physical Actuator Setup: Minimum and Maximum Position along the Rail, Maximum Velocity, Maximal Acceleration, Checking the left Tick-box confirms the Data and when the Data is successfully returned from the Motor the Confirmed Box is checked as well.  
Cues / simpleCue

## The simpleCue Node:

![12](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Cue1.png)

once connected to an Actuator ( via a mixer or adder ) instantiates a series of Fcurves

Vel in Pos Domain   … Velocity over the Distance the Actuator can move
Vel Limit                 … max Acc and max Vel Limit the Velocity over traveled distance 

![13](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Cue2.png)

once the To Time box has been checked 

![14](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Cue3.png)

Two more curves are calculated
Velocity over Time
Acceleration over Time

![15](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Cue4.png)


If those values are within the limits of VelMax and AccMax the cue can be confirmed.

![16](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/Cue5.png)

And the cue can be executed by pushing the right Buttons on the Joystick.

 

#### Remarks

THX to Tintwotin some tips for the install:

"When downloading the Zip from Github, it needs to be unzipped and this part of the name ‘-master’ needs to be removed before zipping it again and then installed.

When enabling the add-on, you’re informed that scipy is missing.

It can be installed very simply with this new & nifty add-on: https://blenderartists.org/t/pip-for-blender/1259938"
