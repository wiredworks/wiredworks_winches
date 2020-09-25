import bpy
import socket
import time
import json

class SFX_OT_CommActOp(bpy.types.Operator):
    """ This operator is the interface between the pysical world, the 3D_View and the Node"""
    bl_idname = "sfx.commactop"
    bl_label = "Actuator Register"

    def modal(self, context, event):
        if event.type == 'TIMER':
            self.MotherNode.TickTime_prop = (time.time_ns() - self.old_time)/1000000.0
            if not(self.MotherNode.operator_started_bit1):                      # destroy
                ret =self.destroy(context)
                return ret
            else:
                self.interact_with_3D_view()

                if (self.MotherNode.actuator_connected_bit1 and                 # connect
                    not(self.MotherNode.actuator_connected_bit2)):
                    # Bit1 (try connect) True Bit2 (connected) False ->
                    # init stuff and setup ports.
                    ret = self.connecting(context)
                    self.old_time = time.time_ns()
                    return ret
                elif (self.MotherNode.actuator_connected_bit1 and               # exchange
                    (self.MotherNode.actuator_connected_bit2)):
                    # Bit1 (try connect) True Bit2 (connected) True ->
                    # excange data
                    ret = self.exchange_data(context)
                    self.old_time = time.time_ns()
                    return ret
                elif (not(self.MotherNode.actuator_connected_bit1) and          # dis-connect
                    (self.MotherNode.actuator_connected_bit2)):
                    # Bit1 (try connect) False Bit2 (connected) True ->
                    # close sockets.
                    ret = self.dis_connect(context)
                    self.old_time = time.time_ns()
                    return ret
                elif (not(self.MotherNode.actuator_connected_bit1) and          # do nothing
                    not(self.MotherNode.actuator_connected_bit2)):
                    # Bit1 (try connect) False Bit2 (connected) False ->
                    # do nothing.
                    pass
                self.old_time = time.time_ns()
                return {'PASS_THROUGH'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        #print('execute')
        context.window_manager.modal_handler_add(self)
        self.old_time = time.time_ns()
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        #print('invoke')
        self.MotherNode = context.active_node
        self.NAME = self.MotherNode.actuator_name
        self.UDP_IP = self.MotherNode.socket_ip
        self.RUDP_PORT = int(self.MotherNode.rsocket_port) 
        self.SUDP_PORT = int(self.MotherNode.ssocket_port)
        self.ID = (self.NAME+'_'+
                   self.UDP_IP+'_'+
                   str(self.RUDP_PORT)+'_'+
                   str(self.SUDP_PORT))
        self.MotherNode.operator_started_bit1 = True

        return self.execute(context)

    def dis_connect(self, context):
        #print('dis-connect')
        try:
            self.rsock.close()
            self.ssock.close()
            del(self.rsock)
            del(self.ssock)
        except AttributeError:
            #print('You tried to disconnect without beeing connected')
            pass
        self.MotherNode.actuator_connected_bit1 = False
        self.MotherNode.actuator_connected_bit2 = False
        self.MotherNode.Actuator_basic_props.online_Actuator = False
        self.MotherNode.Actuator_basic_props.Actuator_props.simple_actuator_confirmed = False
        self.MotherNode.Actuator_basic_props.Actuator_props.simple_actuator_confirm = False
        return {'PASS_THROUGH'}

    def draw(self,context):
        #print('draw')
        self.layout.label(text='You have to restart -- Adress already in use')

    def connecting(self,context):
        #print('connecting')
        socketerr = False
        if hasattr(self,'rsock'):
            self.MotherNode.actuator_connected_bit2 = True
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
            self.MotherNode.actuator_connected_bit2 = True
            return {'PASS_THROUGH'}

    def exchange_data(self,context):
        data = "NO DATA"
        self.MotherNode.Actuator_basic_props.online_Actuator = False
        Message = self.MotherNode.Actuator_basic_props.packSendStringToAxis().encode('utf-8')
        try:
            self.ssock.sendto(Message, (self.UDP_IP, self.SUDP_PORT))
        except AttributeError :
            print('NO SSOCK')

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
            self.MotherNode.Actuator_basic_props.online_Actuator = True
            self.MotherNode.Actuator_basic_props.unpackRecStringfromAxis(data.decode('utf-8'))
        return {'PASS_THROUGH'}

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
        self.MotherNode.actuator_connected_bit1 = False
        self.MotherNode.actuator_connected_bit2 = False
        self.MotherNode.Actuator_basic_props.online_Actuator = False
        self.MotherNode.Actuator_basic_props.Actuator_props.simple_actuator_confirmed = False
        self.MotherNode.Actuator_basic_props.Actuator_props.simple_actuator_confirm = False
        return {'CANCELLED'}
    
    def interact_with_3D_view(self):
        # update DigTwin Props when object is moved in View_3D
        DTwin_startLoc = bpy.data.collections.get("ww SFX_Nodes").children[self.MotherNode.name].\
            objects[self.MotherNode.name+'_In'].location
        DTwin_endLoc = bpy.data.collections.get("ww SFX_Nodes").children[self.MotherNode.name].\
            objects[self.MotherNode.name+'_Out'].location

        bpy.data.collections.get("ww SFX_Nodes").children[self.MotherNode.name].\
            objects[self.MotherNode.name+'_Connector'].constraints['Follow Path'].offset = \
                     self.MotherNode.Actuator_basic_props.ist_Pos *-20 

        self.MotherNode.Actuator_basic_props.\
            DigTwin_basic_props.length = (DTwin_endLoc-DTwin_startLoc).length

        self.MotherNode.Actuator_basic_props.\
            DigTwin_basic_props.start_Loc = DTwin_startLoc

        self.MotherNode.Actuator_basic_props.\
            DigTwin_basic_props.end_Loc = DTwin_endLoc    
