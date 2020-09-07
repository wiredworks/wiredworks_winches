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
            try:
                A = self.Node_Context_ww_data[self.ID]["Destroy"]
            except KeyError:
                return {'PASS_THROUGH'}
            if self.Node_Context_ww_data[self.ID]["Destroy"]:
                self.Node_Context_ww_data.pop(self.ID)
                ret =self.destroy(context)
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
        print('execute')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        print('invoke')
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
        print('dis-connect')
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
        #print('draw')
        self.layout.label(text='You have to restart -- Adress already in use')

    def connecting(self,context):
        print('connecting')
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
        try:
            data, addr = self.rsock.recvfrom(1024) # buffer size is 1024 bytes
        except socket.error as e:
            if e.errno ==10035: #error: [Errno 10035]
                                    # A non-blocking socket operation could
                                    # not be completed immediately --- No Data
                data ="NO DATA"
        if data != "NO DATA":
            message = json.loads(data.decode('utf-8'))

            self.Node_Context_ww_data[self.ID]["Ptime"] =message["Ptime"]
            self.Node_Context_ww_data[self.ID]["X-Soll"]=message["X-Soll"]
            self.Node_Context_ww_data[self.ID]["Y-Soll"]=message["Y-Soll"]
            self.Node_Context_ww_data[self.ID]["Z-Soll"]=message["Z-Soll"]

            self.Node_Context_Active_Node.soll_Pos = float(message["X-Soll"])                

            self.Cube.location.x = self.Node_Context_ww_data[self.ID]["X-Soll"]/ 15000.0 
            self.Cube.location.y = self.Node_Context_ww_data[self.ID]["Y-Soll"]/ 15000.0
            self.Cube.location.z = self.Node_Context_ww_data[self.ID]["Z-Soll"]/ 15000.0
            
            self.Node_Context_ww_data[self.ID]["X-Ist"] = self.Cube.location.x 
            self.Node_Context_ww_data[self.ID]["Y-Ist"] = self.Cube.location.y
            self.Node_Context_ww_data[self.ID]["Z-Ist"] = self.Cube.location.z
            
            ##print(self.SUDP_PORT,
            ##      context.active_node.Shared.ww_data["X-Soll"],
            ##      context.active_node.Shared.ww_data["Y-Soll"],
            ##      context.active_node.Shared.ww_data["Z-Soll"], end ="\r")

        self.Node_Context_ww_data[self.ID]["Btime"] = time.time_ns()
        MESSAGE = json.dumps(self.Node_Context_ww_data[self.ID]).encode('utf-8')
        self.ssock.sendto(MESSAGE, (self.UDP_IP, self.SUDP_PORT))

        return {'PASS_THROUGH'}

    def destroy(self,context):
        print('destroy')
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
