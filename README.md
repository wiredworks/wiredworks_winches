# wiredworks_winches
Dir structure

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
  - space_node.py  (expose some operators to the UI)
  - example.blend
  
/excange_data      (some structures for Data excange)

/operator          (some dialogs and ops not specific to a Node)

/sockets           (Node sockets)

/ui                (node menu)
