import bpy
import socket
import time
import json

class ConnectActuatorOperator(bpy.types.Operator):
    """ This operator Starts the Communication"""
    bl_idname = "ww.start_comm"
    bl_label = "Communication Start"

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.Node_Context_ww_data[self.ID]["EndCommOPerator"]:
                self.Node_Context_ww_data.pop(self.ID)
                ret =self.End_Comm(context)
                return ret
            else:
                if (self.Node_Context_Active_Node.actuator_connected_bit1 and        # connect
                    not(self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) True Bit2 (connected) False ->
                    # init stuff and setup ports.
                    ret = self.connecting(context)
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
        print('Communication Start execute')
        self._timer = context.window_manager.event_timer_add(0.001, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        print('Communication Start invoke')
        if not(context.active_node.operator_started_bit1): 
            self.Node_Context_Active_Node = context.active_node
            self.Node_Context_ww_data =context.active_node.Shared.ww_data
            self.NAME = context.active_node.actuator_name
            self.UDP_IP = context.active_node.socket_ip
            self.RUDP_PORT = int(context.active_node.rsocket_port) 
            self.SUDP_PORT = int(context.active_node.ssocket_port)
            self.ID = (self.NAME+'_'+
                       self.UDP_IP+'_'+
                       str(self.RUDP_PORT)+'_'+
                       str(self.SUDP_PORT))
            self.Node_Context_Active_Node.operator_started_bit1 = True

            self.Node_Context_ww_data[self.ID]={ "Ptime"          : 0,
                                                 "Btime"          : 0,
                                                 "X-Soll"         : -1.0 ,
                                                 "Y-Soll"         : -1.0,
                                                 "Z-Soll"         : -1,
                                                 "X-Ist"          : 0.0,
                                                 "Y-Ist"          : 0.0,
                                                 "Z-Ist"          : 0.0,
                                                 "EndCommOPerator": False,
                                                 "Destroy"        : False}

            return self.execute(context)
        return {'CANCELLED'}

    def dis_connect(self, context):
        print('Communication Start dis-connect')
        return {'PASS_THROUGH'}

    def draw(self,context):
        print('Communication Start draw')

    def connecting(self,context):
        print('Communication Start connecting')
        return {'PASS_THROUGH'}

    def exchange_data(self,context):
        return {'PASS_THROUGH'}

    def End_Comm(self,context):
        print('Communication Start end communication')
        context.window_manager.event_timer_remove(self._timer)
        return {'CANCELLED'}
