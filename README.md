# wiredworks_winches

THX to Tintwotin some tips for the install:

"When downloading the Zip from Github, it needs to be unzipped and this part of the name ‘-master’ needs to be removed before zipping it again and then installed.

When enabling the add-on, you’re informed that scipy is missing.

It can be installed very simply with this new & nifty add-on: https://blenderartists.org/t/pip-for-blender/1259938"


Folder structure

/Node                
  - Actuators   Interface to Motors
  - Clock       To drive the structure
  - Helpers     demuxing, adding, mixxing of signals
  - Kinematics  not yet populated
  - Sensors     Interface to Joystick, and other physical sensors
  
/Node Tree

/UClients_and_helpers
  - clients        (simulated physical motors at different UDP ports)
  - Joystick       (Interface from USB to UDP)
  - space_node.py  (expose some operators to the UI replace the original script in
                    C:\Program Files\Blender Foundation\Blender 2.83\2.83\scripts\startup\bl_ui)
  - example.blend
  
/excange_data      (some structures for Data excange)

/operator          (some ops used in space_node.py)

/sockets           (Node sockets)

/ui                (node menu)
