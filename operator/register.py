import bpy
import socket
import time
import json

class ConnectActuatorOperator(bpy.types.Operator):
    """ This operator registeres the Actuator with The Comm Node"""
    bl_idname = "ww.actuator_register"
    bl_label = "Actuator Register"

    def modal(self, context, event):
        if event.type == 'TIMER':
            self.Node_Context_Active_Node.TickTime_prop = (time.time_ns() - self.old_time)/1000000.0
            try:
                A = self.Node_Context_ww_data[self.ID]["Destroy"]
            except KeyError:
                self.old_time = time.time_ns()
                return {'PASS_THROUGH'}
            # update DigTwin Props when object is moved in View_3D

            ww_DTwin_startLoc = bpy.context.collection.children[context.active_node.name].\
                objects['Rail Actuator_In'].location
            ww_DTwin_endLoc = bpy.context.collection.children[context.active_node.name].\
                objects['Rail Actuator_Out'].location

            self.Node_Context_Active_Node.ww_Actuator_basic_props.\
                ww_DigTwin_basic_props.length = (ww_DTwin_endLoc-ww_DTwin_startLoc).length

            self.Node_Context_Active_Node.ww_Actuator_basic_props.\
                ww_DigTwin_basic_props.start_Loc = ww_DTwin_startLoc

            self.Node_Context_Active_Node.ww_Actuator_basic_props.\
                ww_DigTwin_basic_props.end_Loc = ww_DTwin_endLoc

            
            #Destroy and unload OPerator
            if self.Node_Context_ww_data[self.ID]["Destroy"]:
                self.Node_Context_ww_data.pop(self.ID)
                ret =self.destroy(context)
                self.old_time = time.time_ns()
                return ret
            else:
                #connect
                if (self.Node_Context_Active_Node.actuator_connected_bit1 and        # connect
                    not(self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) True Bit2 (connected) False ->
                    # init stuff and setup ports.
                    ret = self.connecting(context)
                    self.old_time = time.time_ns()
                    return ret
                #exchange
                elif (self.Node_Context_Active_Node.actuator_connected_bit1 and      # exchange
                    (self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) True Bit2 (connected) True ->
                    # excange data
                    ret = self.exchange_data(context)
                    self.old_time = time.time_ns()
                    return ret
                #close USockets 
                elif (not(self.Node_Context_Active_Node.actuator_connected_bit1) and # dis-connect
                    (self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) False Bit2 (connected) True ->
                    # close sockets.
                    ret = self.dis_connect(context)
                    self.old_time = time.time_ns()
                    return ret
                #do nothing
                elif (not(self.Node_Context_Active_Node.actuator_connected_bit1) and # do nothing
                    not(self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) False Bit2 (connected) False ->
                    # do nothing.
                    #print('nothing')                 
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
        self.Node_Context_Active_Node.actuator_registered_bit1 = True

        self.Node_Context_ww_data[self.ID]={ "Ptime"           : 0,
                                                "Btime"           : 0,
                                                "X-Soll"          : -1.0 ,
                                                "Y-Soll"          : -1.0,
                                                "Z-Soll"          : -1,
                                                "X-Ist"           : 0.0,
                                                "Y-Ist"           : 0.0,
                                                "Z-Ist"           : 0.0,
                                                "EndCommOPerator" : False,
                                                "Destroy"         : False}

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
        self.Node_Context_Active_Node.actuator_connected_bit1 = False
        self.Node_Context_Active_Node.actuator_connected_bit2 = False
        self.Node_Context_Active_Node.Actuator_basic_props.online_Actuator = False
        self.Node_Context_Active_Node.Actuator_basic_props.ww_Actuator_props.simple_actuator_confirmed = False
        self.Node_Context_Active_Node.Actuator_basic_props.ww_Actuator_props.simple_actuator_confirm = False
        return {'PASS_THROUGH'}

    def draw(self,context):
        #print('draw')
        self.layout.label(text='You have to restart -- Adress already in use')

    def connecting(self,context):
        #print('connecting')
        socketerr = False
        if hasattr(self,'rsock'):
            self.Node_Context_Active_Node.actuator_connected_bit2 = True
            return {'PASS_THROUGH'}

        self.rsock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP

        self.ssock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP

        if self.RUDP_PORT == 15021:
            self.Cube = bpy.data.objects["Cube"]
        elif self.RUDP_PORT == 15023:
            self.Cube = bpy.data.objects["Cube.001"]
        else:
            self.Cube = bpy.data.objects["Cube.002"]

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
        self.Node_Context_Active_Node.Actuator_basic_props.online_Actuator = False
        Message = self.Node_Context_Active_Node.Actuator_basic_props.packSendStringToAxis().encode('utf-8')
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
            self.Node_Context_Active_Node.Actuator_basic_props.online_Actuator = True
            self.Node_Context_Active_Node.Actuator_basic_props.unpackRecStringfromAxis(data.decode('utf-8'))
            # self.Node_Context_ww_data[self.ID]["Ptime"] =message["Ptime"]
            # self.Node_Context_ww_data[self.ID]["X-Soll"]=message["X-Soll"]
            # self.Node_Context_ww_data[self.ID]["Y-Soll"]=message["Y-Soll"]
            # self.Node_Context_ww_data[self.ID]["Z-Soll"]=message["Z-Soll"]             

            # self.Cube.location.x = self.Node_Context_ww_data[self.ID]["X-Soll"]/ 15000.0 
            # self.Cube.location.y = self.Node_Context_ww_data[self.ID]["Y-Soll"]/ 15000.0
            # self.Cube.location.z = self.Node_Context_ww_data[self.ID]["Z-Soll"]/ 15000.0
            
            # self.Node_Context_ww_data[self.ID]["X-Ist"] = self.Cube.location.x 
            # self.Node_Context_ww_data[self.ID]["Y-Ist"] = self.Cube.location.y
            # self.Node_Context_ww_data[self.ID]["Z-Ist"] = self.Cube.location.z
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
        self.Node_Context_Active_Node.actuator_connected_bit1 = False
        self.Node_Context_Active_Node.actuator_connected_bit2 = False
        self.Node_Context_Active_Node.Actuator_basic_props.online_Actuator = False
        self.Node_Context_Active_Node.Actuator_basic_props.ww_Actuator_props.simple_actuator_confirmed = False
        self.Node_Context_Active_Node.Actuator_basic_props.ww_Actuator_props.simple_actuator_confirm = False
        return {'PASS_THROUGH'}
