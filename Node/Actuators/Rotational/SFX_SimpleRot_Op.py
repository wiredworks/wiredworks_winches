import bpy
import socket
import time
import json

from math import radians

from .... exchange_data.sfx import sfx
from .SFX_SimpleRot_Data import actuator_simplerot

class SFX_OT_SimpleRot_Op(bpy.types.Operator):
    """ This operator is the interface between the pysical world, the 3D_View and the Node"""
    bl_idname = "sfx.simplerot_op"
    bl_label = "Actuator Register"

    i = 0

    def modal(self, context, event):
        if event.type == 'TIMER':
            self.i = self.i+1
            try:
                sfx.actuators[self.MotherNode.name].TickTime_prop = (time.time_ns() - self.old_time)/100000.0
            except KeyError:
                self.sfx_entry_exists = False
                self.End_Comm(context)
                return {'CANCELLED'}
            if self.sfx_entry_exists:
                self.MotherNode.sfx_update()
                if not(sfx.actuators[self.MotherNode.name].operator_started):
                    sfx.actuators[self.MotherNode.name].operator_running_modal = False
                    self.End_Comm(context)                                           # End_Comm
                    return {'CANCELLED'}
                else:
                    sfx.actuators[self.MotherNode.name].operator_running_modal = True 

                if (self.HardMaxOld !=sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop or
                    self.HardMinOld !=sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop or
                    self.VelMaxOld  !=sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop or
                    self.AccMaxOld  !=sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop):
                    sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_confirm = False
                    sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_confirmed = False
                self.HardMaxOld =sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
                self.HardMinOld =sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
                self.VelMaxOld  =sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop
                self.AccMaxOld  =sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop

                self.interact_with_3D_view()

                if (sfx.actuators[self.MotherNode.name].actuator_connected_bit1 and
                    not(sfx.actuators[self.MotherNode.name].actuator_connected_bit2)):
                    # Bit1 (try connect) True Bit2 (connected) False ->                          # connect
                    ret = self.connect(context)
                    self.old_time = time.time_ns()
                    return ret
                elif (sfx.actuators[self.MotherNode.name].actuator_connected_bit1 and
                    (sfx.actuators[self.MotherNode.name].actuator_connected_bit2)):
                    # Bit1 (try connect) True Bit2 (connected) True ->                            # exchange data
                    ret = self.exchange_data(context)
                    self.old_time = time.time_ns()
                    return ret
                elif (not(sfx.actuators[self.MotherNode.name].actuator_connected_bit1) and
                    (sfx.actuators[self.MotherNode.name].actuator_connected_bit2)):
                    # Bit1 (try connect) False Bit2 (connected) True ->                            # close sockets.
                    ret = self.dis_connect(context)
                    self.old_time = time.time_ns()
                    return ret
                elif (not(sfx.actuators[self.MotherNode.name].actuator_connected_bit1) and
                    not(sfx.actuators[self.MotherNode.name].actuator_connected_bit2)):
                    # Bit1 (try connect) False Bit2 (connected) False ->                           # do nothing.
                    pass
                self.old_time = time.time_ns()
                return {'PASS_THROUGH'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        self.sfx_entry_exists = True
        self.MotherNode = context.active_node
        self.old_time = time.time_ns()
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.sfx_entry_exists = True
        self.MotherNode = context.active_node
        if not(sfx.actuators[self.MotherNode.name].operator_running_modal):
            self.NAME      = sfx.actuators[self.MotherNode.name].actuator_name
            self.UDP_IP    = sfx.actuators[self.MotherNode.name].socket_ip
            self.RUDP_PORT = int(sfx.actuators[self.MotherNode.name].rsocket_port) 
            self.SUDP_PORT = int(sfx.actuators[self.MotherNode.name].ssocket_port)
            self.ID = (self.NAME+'_'+
                       self.UDP_IP+'_'+
                       str(self.RUDP_PORT)+'_'+
                       str(self.SUDP_PORT))       
            self.HardMaxOld =0.0
            self.HardMinOld =0.0
            self.VelMaxOld  =0.0
            self.AccMaxOld  =0.0
            return self.execute(context)
        else:
            return {'CANCELLED'}

    def draw(self,context):
        self.layout.label(text='You have to restart -- Adress already in use')

    def connect(self,context):
        #print('connecting')
        socketerr = False
        if hasattr(self,'rsock'):
            sfx.actuators[self.MotherNode.name].actuator_connected_bit2 = True
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
                self.End_Comm(context)
                socketerr = True
        if socketerr:
            sfx.actuators[self.MotherNode.name].actuator_connected_bit2 = False
            return {'PASS_THROUGH'}
        else:
            sfx.actuators[self.MotherNode.name].actuator_connected_bit2 = True
            return {'PASS_THROUGH'}

    def exchange_data(self,context):
        data = "NO DATA"
        sfx.actuators[self.MotherNode.name].online_Actuator = False

        Message = sfx.actuators[self.MotherNode.name].Actuator_basic_props.packSendStringToAxis().encode('utf-8')
        try:
            self.ssock.sendto(Message, (self.UDP_IP, self.SUDP_PORT))
        except AttributeError :
            #print('NO SSOCK')
            pass
        try:
            data, addr = self.rsock.recvfrom(500) # buffer size is 1024 bytes
        except socket.error as e:
            if e.errno ==10035: #error: [Errno 10035]
                                    # A non-blocking socket operation could
                                    # not be completed immediately --- No Data
                data ="NO DATA"
        except AttributeError :
            #print('NO RSOCK')
            pass
        if data != "NO DATA":
            sfx.actuators[self.MotherNode.name].Actuator_basic_props.online_Actuator = True
            sfx.actuators[self.MotherNode.name].Actuator_basic_props.unpackRecStringfromAxis(data.decode('utf-8'))
        
        sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop = \
            min(sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop, \
            sfx.actuators[self.MotherNode.name].Actuator_basic_props.DigTwin_basic_props.end_Rot)

        sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop = \
            max(sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop, \
            sfx.actuators[self.MotherNode.name].Actuator_basic_props.DigTwin_basic_props.start_Rot)
        
        return {'PASS_THROUGH'}

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
        sfx.actuators[self.MotherNode.name].actuator_connected_bit1 = False
        sfx.actuators[self.MotherNode.name].actuator_connected_bit2 = False
        sfx.actuators[self.MotherNode.name].Actuator_basic_props.online_Actuator = False
        sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_confirmed = False
        sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_confirm = False
        return {'PASS_THROUGH'}

    def End_Comm(self,context):
        #print('destroy')
        try:
            self.rsock.close()
            self.ssock.close()
            del(self.rsock)
            del(self.ssock)
        except AttributeError:
            #print('You tried to disconnect without beeing connected')
            pass
        if self.sfx_entry_exists:
            sfx.actuators[self.MotherNode.name].actuator_connected_bit1 = False
            sfx.actuators[self.MotherNode.name].actuator_connected_bit2 = False
            sfx.actuators[self.MotherNode.name].Actuator_basic_props.online_Actuator = False
            sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_confirmed = False
            sfx.actuators[self.MotherNode.name].Actuator_basic_props.Actuator_props.simple_actuator_confirm = False
        return {'CANCELLED'}
    
    def interact_with_3D_view(self):
        # update DigTwin Props when object is moved in View_3D
        pass
        DTwin_startLoc = bpy.data.collections.get("ww SFX_Nodes").children[self.MotherNode.name].\
            objects[self.MotherNode.name+'_In'].matrix_world.to_translation()
        DTwin_endLoc = bpy.data.collections.get("ww SFX_Nodes").children[self.MotherNode.name].\
            objects[self.MotherNode.name+'_Out'].matrix_world.to_translation()

        bpy.data.collections.get("ww SFX_Nodes").children[self.MotherNode.name].\
            objects[self.MotherNode.name+'_Connector'].\
            rotation_euler.rotate_axis("Z", radians(sfx.actuators[self.MotherNode.name].Actuator_basic_props.ist_Pos))

        DTwin_conLoc = bpy.data.collections.get("ww SFX_Nodes").children[self.MotherNode.name].\
            objects[self.MotherNode.name+'_Connector'].matrix_world.to_translation()

        sfx.actuators[self.MotherNode.name].Actuator_basic_props.\
            DigTwin_basic_props.length =  sfx.actuators[self.MotherNode.name].Actuator_basic_props.\
            DigTwin_basic_props.end_Rot - sfx.actuators[self.MotherNode.name].Actuator_basic_props.\
            DigTwin_basic_props.start_Rot

        sfx.actuators[self.MotherNode.name].Actuator_basic_props.\
            DigTwin_basic_props.start_Loc = DTwin_startLoc

        sfx.actuators[self.MotherNode.name].Actuator_basic_props.\
            DigTwin_basic_props.end_Loc = DTwin_endLoc

        sfx.actuators[self.MotherNode.name].Actuator_basic_props.\
            DigTwin_basic_props.con_Loc = DTwin_conLoc
