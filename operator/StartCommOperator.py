import bpy
import socket
import time
import json

from ..Node.ww_ActuatorStartCommNode import ww_ActuatorStartCommNode
from ..exchange_data.ww_Joystick_props import ww_Joystick_props

class ConnectActuatorOperator(bpy.types.Operator):
    """ This operator Starts the Communication"""
    bl_idname = "ww.start_comm"
    bl_label = "Communication Start"

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.Node_Context_ww_Joy[self.ID]["EndCommOPerator"]:
                self.Node_Context_ww_Joy.pop(self.ID)
                ret =self.End_Comm(context)
                return ret
            else:
                if (self.Node_Context_Active_Node.actuator_connected_bit1 and        # connect
                    not(self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) True Bit2 (connected) False ->
                    # init stuff and setup ports.
                    ret = self.connect(context)
                    return ret
                elif (self.Node_Context_Active_Node.actuator_connected_bit1 and      # exchange
                    (self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) True Bit2 (connected) True ->
                    # excange data
                    ret = self.exchange_data(context)
                    return ret
                elif (not(self.Node_Context_Active_Node.actuator_connected_bit1) and # dis-connect
                    (self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) False Bit2 (connected) True ->
                    # close sockets.
                    ret = self.dis_connect(context)
                    return ret
                elif (not(self.Node_Context_Active_Node.actuator_connected_bit1) and # do nothing
                    not(self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) False Bit2 (connected) False ->
                    # do nothing.
                    #print('nothing')                 
                    pass
                return {'PASS_THROUGH'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        print('Communication Start -- execute')
        self._timer = context.window_manager.event_timer_add(0.001, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        print('Communication Start -- invoke')
        if not(context.active_node.operator_started_bit1): 
            self.Node_Context_Active_Node = context.active_node
            #self.Node_Context_ww_data =context.active_node.Shared.ww_data
            self.Node_Context_ww_Joy  =context.active_node.Shared.ww_Joy
            self.Node_Context_Active_Node_Joystick_props = context.active_node.ww_Joystick_props
            self.NAME = context.active_node.actuator_name
            self.UDP_IP = context.active_node.socket_ip
            self.RUDP_PORT = int(context.active_node.rsocket_port) 
            self.SUDP_PORT = int(context.active_node.ssocket_port)
            self.ID = (self.NAME+'_'+
                       self.UDP_IP+'_'+
                       str(self.RUDP_PORT)+'_'+
                       str(self.SUDP_PORT))
            self.Node_Context_Active_Node.operator_started_bit1 = True

            self.Node_Context_ww_Joy[self.ID]={ 'Ptime'             : 0,
                                                'Btime'             : 0,
                                                'X-Achse'           : 0,
                                                'Y-Achse'           : 0,
                                                'Z-Achse'           : 0,
                                                'X-Rot'             : 0,
                                                'Y-Rot'             : 0,
                                                'Z-Rot'             : 0,
                                                'Slider'            : 0,
                                                'Buttons'           : 0,
                                                'HAT-Switch'        : 0,
                                                'EndCommOPerator'   : False,
                                                'Destroy'           : False}

            return self.execute(context)
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
        self.Node_Context_Active_Node.actuator_connected_bit1 = False
        self.Node_Context_Active_Node.actuator_connected_bit2 = False
        return {'PASS_THROUGH'}

    def draw(self,context):
        print('Communication -- Start draw')

    def connect(self,context):
        print('Communication Start -- connect')
        socketerr = False
        if hasattr(self,'rsock'):
            self.Node_Context_Active_Node.actuator_connected_bit2 = True
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
            self.Node_Context_Active_Node.actuator_connected_bit2 = True
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
            self.Node_Context_ww_Joy[self.ID]["Ptime"]                  =message['Ptime']
            self.Node_Context_ww_Joy[self.ID]["Btime"]                  =message['Btime']
            self.Node_Context_ww_Joy[self.ID]["X-Achse"]                =message['X-Achse']
            self.Node_Context_ww_Joy[self.ID]["X-Achse"]                =message['Y-Achse']
            self.Node_Context_ww_Joy[self.ID]["X-Achse"]                =message['Z-Achse']
            self.Node_Context_ww_Joy[self.ID]["X-Rot"]                  =message['X-Rot']
            self.Node_Context_ww_Joy[self.ID]["X-Rot"]                  =message['Y-Rot']
            self.Node_Context_ww_Joy[self.ID]["X-Rot"]                  =message['Z-Rot']
            self.Node_Context_ww_Joy[self.ID]["Slider"]                 =message['Slider']
            self.Node_Context_ww_Joy[self.ID]["Buttons"]                =message['Buttons']
            self.Node_Context_ww_Joy[self.ID]["HAT-Switch"]             =message['HAT-Switch']
            # excange Data with Node
            self.Node_Context_Active_Node_Joystick_props.Ptime          =message["Ptime"]
            self.Node_Context_Active_Node_Joystick_props.Btime          =message["Btime"]
            self.Node_Context_Active_Node_Joystick_props.X_Achse        =message["X-Achse"]
            self.Node_Context_Active_Node_Joystick_props.Y_Achse        =message["Y-Achse"]
            self.Node_Context_Active_Node_Joystick_props.Z_Achse        =message["Z-Achse"]
            self.Node_Context_Active_Node_Joystick_props.X_Rot          =message["X-Rot"]
            self.Node_Context_Active_Node_Joystick_props.Y_Rot          =message["Y-Rot"]
            self.Node_Context_Active_Node_Joystick_props.Z_Rot          =message["Z-Rot"]
            self.Node_Context_Active_Node_Joystick_props.Slider         =message["Slider"]
            self.Node_Context_Active_Node_Joystick_props.HAT_Switch     =message["HAT-Switch"]
            self.Node_Context_Active_Node_Joystick_props.EndCommOPerator=message["EndCommOPerator"]
            self.Node_Context_Active_Node_Joystick_props.Destroy        =message["Destroy"]
            self.Node_Context_Active_Node_Joystick_props.Button1        =message['Buttons'][0]
            self.Node_Context_Active_Node_Joystick_props.Button2        =message['Buttons'][1]
            self.Node_Context_Active_Node_Joystick_props.Button3        =message['Buttons'][2]
            self.Node_Context_Active_Node_Joystick_props.Button4        =message['Buttons'][3]
            self.Node_Context_Active_Node_Joystick_props.Button5        =message['Buttons'][4]
            self.Node_Context_Active_Node_Joystick_props.Button6        =message['Buttons'][5]
            self.Node_Context_Active_Node_Joystick_props.Button7        =message['Buttons'][6]
            self.Node_Context_Active_Node_Joystick_props.Button8        =message['Buttons'][7]
            self.Node_Context_Active_Node_Joystick_props.Button9        =message['Buttons'][8]
            self.Node_Context_Active_Node_Joystick_props.Button10       =message['Buttons'][9]
            self.Node_Context_Active_Node_Joystick_props.Button11       =message['Buttons'][10]
            self.Node_Context_Active_Node_Joystick_props.Button12       =message['Buttons'][11]
            # excange Data with output
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Ptime          =message["Ptime"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Btime          =message["Btime"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.X_Achse        =message["X-Achse"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Y_Achse        =message["Y-Achse"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Z_Achse        =message["Z-Achse"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.X_Rot          =message["X-Rot"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Y_Rot          =message["Y-Rot"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Z_Rot          =message["Z-Rot"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Slider         =message["Slider"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.HAT_Switch     =message["HAT-Switch"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.EndCommOPerator=message["EndCommOPerator"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Destroy        =message["Destroy"]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button1        =message['Buttons'][0]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button2        =message['Buttons'][1]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button3        =message['Buttons'][2]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button4        =message['Buttons'][3]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button5        =message['Buttons'][4]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button6        =message['Buttons'][5]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button7        =message['Buttons'][6]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button8        =message['Buttons'][7]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button9        =message['Buttons'][8]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button10       =message['Buttons'][9]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button11       =message['Buttons'][10]
            self.Node_Context_Active_Node.outputs["Joy Values"].default_value.Button12       =message['Buttons'][11]
            # Set Joy Float to X-Achse
            self.Node_Context_Active_Node.outputs["Joy Float"].default_value = message['X-Achse']
            # Trigger update and show Tick Time
            self.Node_Context_Active_Node.TickTime_prop = (time.time_ns()-message["Ptime"])/1000000.0

        self.Node_Context_ww_Joy[self.ID]["Btime"] = time.time_ns()
        MESSAGE = json.dumps(self.Node_Context_ww_Joy[self.ID]).encode('utf-8')
        try:
            self.ssock.sendto(MESSAGE, (self.UDP_IP, self.SUDP_PORT))
        except AttributeError :
            print('NO SSOCK')
        return {'PASS_THROUGH'}

    def End_Comm(self,context):
        print('Communication Start -- end communication')
        context.window_manager.event_timer_remove(self._timer)
        return {'CANCELLED'}
