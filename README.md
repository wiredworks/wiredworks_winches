# wiredworks_winches

Menu Tree New Structure

To Test:

Outside Blender:

Start UClients_and_Helpers\Joystick17

a window with joystick raw values is opened  

Start UClients_and_Helpers\Client_at_1521

a window showing the properties of a simple physical axis

In Blender:

Node Editor: ww SFX_Nodes

Add Clock Node    -> a New Collection 'ww SFX_Nodes is created

Add Sensors/JoystickNode

Add Helpers/JoyDemuxNode

Add Actuators/RailNode -> inside the ww SFX_Node collection a new collection is created.

connect: JoystickNode 'Joy Values' to 'Joy In' of the demuxer select 'Stick' to any of the Joystick axis, Button1 and Button2 likewise

connect 'Stick' of the demuxer with 'SetVel' of the 'Simple Rail Actuator' and the Buttons to 'select' and 'anable'

set 'Expand Basic Data'

set 'Expand Digital Twin Basic'

set 'Expand Physical Actuator Setup'

Start the clock

Register the Joystick  'Time Tick' will start

Start the 'Demuxer'  the 2 Tick Boxes will get set and the 'Time Tick' will start 

Register the 'Simple Rail Actuator' 'Time Tick' will start

Tick the left TickBox of the Joystick -> The Server is started and will receive Values from the Joystick 

Tick the left TickBox of the Actuator -> The Server starts to communicate with Client_at_15021

Confirm the 'Simple Physical Actuator Setup' by ticking the left TickBox


On The Joystick push the Buttons and wiggle the stick and the Connector of the Rail Actuator will move

EXPERIMENT!




