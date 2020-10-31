import bpy
import socket
import time
import json

from ....exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset

from .... exchange_data.sfx import sfx
from .... exchange_data.sfx import sfx_sensor

class SFX_OT_Joystick_Op(bpy.types.Operator):
    """ This operator takes the Input of a Joystick"""
    bl_idname = "sfx.joystick_op"
    bl_label = "Joystick Input"

    def modal(self, context, event):
        if event.type == 'TIMER':
            #print((time.time_ns() - self.old_time)/100000.0)
            try:
                sfx.sensors[self.MotherNode.name].TickTime_prop = (time.time_ns() - self.old_time)/100000.0
                self.MotherNode.sfx_update()
            except KeyError:
                self.sfx_entry_exists = False
                ret =self.End_Comm(context)
                return ret
            if self.sfx_entry_exists:
                sfx.sensors[self.MotherNode.name].TickTime_prop = (time.time_ns() - self.old_time)/1000000.0
                if not(sfx.sensors[self.MotherNode.name].operator_registered):             # destroy
                    ret =self.End_Comm(context)
                    return ret
                else: 
                    if (sfx.sensors[self.MotherNode.name].actuator_connected_bit1 and        # connect
                        not(sfx.sensors[self.MotherNode.name].actuator_connected_bit2)):
                        # Bit1 (try connect) True Bit2 (connected) False ->
                        # init stuff and setup ports.
                        ret = self.connect(context)
                        self.old_time = time.time_ns()
                        return ret
                    elif (sfx.sensors[self.MotherNode.name].actuator_connected_bit1 and      # exchange
                        (sfx.sensors[self.MotherNode.name].actuator_connected_bit2)):
                        # Bit1 (try connect) True Bit2 (connected) True ->
                        # excange data
                        ret = self.exchange_data(context)
                        self.old_time = time.time_ns()
                        return ret
                    elif (sfx.sensors[self.MotherNode.name].actuator_connected_bit1 and     #dis-connect
                        (sfx.sensors[self.MotherNode.name].actuator_connected_bit2)):
                        # Bit1 (try connect) False Bit2 (connected) True ->
                        # close sockets.
                        ret = self.dis_connect(context)
                        self.old_time = time.time_ns()
                        return ret
                    elif (sfx.sensors[self.MotherNode.name].actuator_connected_bit1 and      # do nothing
                        not(sfx.sensors[self.MotherNode.name].actuator_connected_bit2)):
                        # Bit1 (try connect) False Bit2 (connected) False ->
                        # do nothing.
                        #print('nothing')                 
                        pass
                    self.old_time = time.time_ns()
                    return {'PASS_THROUGH'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        self.old_time = time.time_ns()
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.sfx_entry_exists = True
        self.MotherNode = context.active_node
        if not(sfx.sensors[self.MotherNode.name].operator_registered):            
            sfx.sensors[self.MotherNode.name].operator_registered = True

            self.NAME      = sfx.sensors[self.MotherNode.name].actuator_name
            self.UDP_IP    = sfx.sensors[self.MotherNode.name].socket_ip
            self.RUDP_PORT = int(sfx.sensors[self.MotherNode.name].rsocket_port) 
            self.SUDP_PORT = int(sfx.sensors[self.MotherNode.name].ssocket_port)
            self.ID = (self.NAME+'_'+
                       self.UDP_IP+'_'+
                       str(self.RUDP_PORT)+'_'+
                       str(self.SUDP_PORT))           

            self.Joy_Data={  'Ptime'  : 0,'Btime'  : 0,
                             'X-Achse': 0,'Y-Achse': 0,'Z-Achse'   : 0,
                             'X-Rot'  : 0,'Y-Rot'  : 0,'Z-Rot'     : 0,
                             'Slider' : 0,'Buttons': 0,'HAT-Switch': 0,
                             'EndCommOPerator': False,'Destroy'    : False}
            return self.execute(context)
        else:
            return {'CANCELLED'}

    def dis_connect(self, context):
        print('Communication Start -- dis-connect')
        try:
            self.rsock.close()
            self.ssock.close()
            del(self.rsock)
            del(self.ssock)
        except AttributeError:
            #print('You tried to disconnect without beeing connected')
            pass
        sfx.sensors[self.MotherNode.name].actuator_connected_bit1 = False
        sfx.sensors[self.MotherNode.name].actuator_connected_bit2 = False
        return {'PASS_THROUGH'}

    def draw(self,context):
        print('Communication -- Start draw')

    def connect(self,context):
        print('Communication Start -- connect')
        socketerr = False
        if hasattr(self,'rsock'):
            sfx.sensors[self.MotherNode.name].actuator_connected_bit2 = True
            return {'PASS_THROUGH'}

        self.rsock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP

        self.ssock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP

        try:
            self.rsock.bind((self.UDP_IP, self.RUDP_PORT))
            self.rsock.setblocking(0)    
        except socket.error as e:
            if e.errno == 10048:
                self.destroy(context)
                socketerr = True
        if socketerr:
            return {'PASS_THROUGH'}
        else:
            sfx.sensors[self.MotherNode.name].actuator_connected_bit2 = True
            return {'PASS_THROUGH'}

    def exchange_data(self,context):
        data = "NO DATA" 
        try:
            data, addr = self.rsock.recvfrom(1024) # buffer size is 1024 bytes
        except socket.error as e:
            if e.errno ==10035: #error: [Errno 10035]
                                    # A non-blocking socket operation could
                                    # not be completed immediately --- No Data
                data ="NO DATA"
        except AttributeError :
            print('NO RSOCK')
        if data != "NO DATA":
            message = json.loads(data.decode('utf-8'))
            # exchange Data with Python Joystick Input
            self.Joy_Data["Ptime"]                  =message['Ptime']
            self.Joy_Data["Btime"]                  =message['Btime']
            self.Joy_Data["X-Achse"]                =message['X-Achse']
            self.Joy_Data["Y-Achse"]                =message['Y-Achse']
            self.Joy_Data["Z-Achse"]                =message['Z-Achse']
            self.Joy_Data["X-Rot"]                  =message['X-Rot']
            self.Joy_Data["Y-Rot"]                  =message['Y-Rot']
            self.Joy_Data["Z-Rot"]                  =message['Z-Rot']
            self.Joy_Data["Slider"]                 =message['Slider']
            self.Joy_Data["Buttons"]                =message['Buttons']
            self.Joy_Data["HAT-Switch"]             =message['HAT-Switch']
            # excange Data with Node
            sfx.sensors[self.MotherNode.name].Joystick_props.X_Achse        =(float(message["X-Achse"])/32768.0)*100
            sfx.sensors[self.MotherNode.name].Joystick_props.Y_Achse        =(float(message["Y-Achse"])/32768.0)*100
            sfx.sensors[self.MotherNode.name].Joystick_props.Z_Achse        =(float(message["Z-Achse"])/32768.0)*100
            sfx.sensors[self.MotherNode.name].Joystick_props.X_Rot          =(float(message["X-Rot"])/32768.0)*100
            sfx.sensors[self.MotherNode.name].Joystick_props.Y_Rot          =(float(message["Y-Rot"])/32768.0)*100
            sfx.sensors[self.MotherNode.name].Joystick_props.Z_Rot          =(float(message["Z-Rot"])/32768.0)*100
            sfx.sensors[self.MotherNode.name].Joystick_props.Slider         =(float(message["Slider"])/32768.0)*100
            sfx.sensors[self.MotherNode.name].Joystick_props.HAT_Switch     =message["HAT-Switch"]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button1        =message['Buttons'][0]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button2        =message['Buttons'][1]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button3        =message['Buttons'][2]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button4        =message['Buttons'][3]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button5        =message['Buttons'][4]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button6        =message['Buttons'][5]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button7        =message['Buttons'][6]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button8        =message['Buttons'][7]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button9        =message['Buttons'][8]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button10       =message['Buttons'][9]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button11       =message['Buttons'][10]
            sfx.sensors[self.MotherNode.name].Joystick_props.Button12       =message['Buttons'][11]

        MESSAGE = json.dumps(self.Joy_Data).encode('utf-8')
        try:
            self.ssock.sendto(MESSAGE, (self.UDP_IP, self.SUDP_PORT))
        except AttributeError :
            print('NO SSOCK')

        return {'PASS_THROUGH'}

    def End_Comm(self,context):        
        print('Communication Start -- end-communication')
        try:
            self.rsock.close()
            self.ssock.close()
            del(self.rsock)
            del(self.ssock)
        except AttributeError:
            #print('You tried to disconnect without beeing connected')
            pass
        print('Communication Start -- end timer')
        #context.window_manager.event_timer_remove(self._timer)
        return {'CANCELLED'}

    def destroy(self,context):
        #print('destroy')
        try:
            self.rsock.close()
            self.ssock.close()
            del(self.rsock)
            del(self.ssock)
        except AttributeError:
            #print('You tried to disconnect without beeing connected')
            pass
        sfx.sensors[self.MotherNode.name].actuator_connected_bit1 = False
        sfx.sensors[self.MotherNode.name].actuator_connected_bit2 = False
        return {'CANCELLED'}
