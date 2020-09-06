import bpy
import socket
import time
import json

class ConnectActuatorOperator(bpy.types.Operator):
    """ This operator connects the Actuator"""
    bl_idname = "ww.actuator_connect"
    bl_label = "Actuator Connect"

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.Node_Context_ww_data["Destroy"]:
                self.cancel(context)
            else:
                if (self.Node_Context_Active_Node.actuator_connected_bit1 and
                    not(self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) True Bit2 (connected) False ->
                    # init stuff and setup ports.
                    self.connecting(context)
                elif (self.Node_Context_Active_Node.actuator_connected_bit1 and
                    (self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) True Bit2 (connected) True ->
                    # excange data
                    self.excange_data(context)
                elif (not(self.Node_Context_Active_Node.actuator_connected_bit1) and
                    (self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) False Bit2 (connected) True ->
                    # close sockets.
                    self.disconnect(context)
                elif (not(self.Node_Context_Active_Node.actuator_connected_bit1) and
                    not(self.Node_Context_Active_Node.actuator_connected_bit2)):
                    # Bit1 (try connect) False Bit2 (connected) False ->
                    # do nothing.
                    #print('nothing')                 
                    pass
        return {'PASS_THROUGH'}

    def execute(self, context):
        #print('EXECUTE')
        self._timer = context.window_manager.event_timer_add(0.001, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        #print('INVOKE')
        if not(context.active_node.operator_started_bit1): 
            self.Node_Context_Active_Node = context.active_node
            self.Node_Context_ww_data =context.active_node.Shared.ww_data
            self.UDP_IP = context.active_node.socket_ip
            self.RUDP_PORT = int(context.active_node.rsocket_port) 
            self.SUDP_PORT = int(context.active_node.ssocket_port)
            self.Node_Context_Active_Node.operator_started_bit1 = True
            return self.execute(context)
        return {'FINISHED'}

    def cancel(self, context):
        print('CANCEL')
        self.Node_Context_ww_data["Destroy"] = False
        try:
            self.rsock.close()
            self.ssock.close()
        except AttributeError:
            #print('You tried to disconnect without beeing connected')
            pass
        context.window_manager.event_timer_remove(self._timer)
        return {'FINISHED'}

    def draw(self,context):
        #print('draw')
        self.layout.label(text='Adress already in use --- Connect canceled')

    def connecting(self,context):
        #print('connecting')
        if hasattr(self,'rsock'):
            self.Node_Context_Active_Node.actuator_connected_bit2 = True
            return {'PASS_THROUGH'}

        self.rsock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP

        self.ssock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP

        if self.RUDP_PORT == 15021:
            self.Cube = bpy.data.objects["Cube"]
        else:
            self.Cube = bpy.data.objects["Cube.001"]

        try:
            self.rsock.bind((self.UDP_IP, self.RUDP_PORT))
            self.rsock.setblocking(0)    
        except socket.error as e:
            if e.errno == 10048:
                wm = context.window_manager
                r = wm.invoke_props_dialog(self)
                self.disconnect(context)
                return r
        self.Node_Context_Active_Node.actuator_connected_bit2 = True

        return {'PASS_THROUGH'}

    def excange_data(self,context):
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

            self.Node_Context_ww_data["Ptime"] =message["Ptime"]
            self.Node_Context_ww_data["X-Soll"]=message["X-Soll"]
            self.Node_Context_ww_data["Y-Soll"]=message["Y-Soll"]
            self.Node_Context_ww_data["Z-Soll"]=message["Z-Soll"]

            self.Node_Context_Active_Node.soll_Pos = float(message["X-Soll"])                

            self.Cube.location.x = self.Node_Context_ww_data["X-Soll"]/ 15000.0 
            self.Cube.location.y = self.Node_Context_ww_data["Y-Soll"]/ 15000.0
            self.Cube.location.z = self.Node_Context_ww_data["Z-Soll"]/ 15000.0
            
            self.Node_Context_ww_data["X-Ist"] = self.Cube.location.x 
            self.Node_Context_ww_data["Y-Ist"] = self.Cube.location.y
            self.Node_Context_ww_data["Z-Ist"] = self.Cube.location.z
            
            ##print(self.SUDP_PORT,
            ##      context.active_node.Shared.ww_data["X-Soll"],
            ##      context.active_node.Shared.ww_data["Y-Soll"],
            ##      context.active_node.Shared.ww_data["Z-Soll"], end ="\r")

        self.Node_Context_ww_data["Btime"] = time.time_ns()
        MESSAGE = json.dumps(self.Node_Context_ww_data).encode('utf-8')
        self.ssock.sendto(MESSAGE, (self.UDP_IP, self.SUDP_PORT))

        return {'PASS_THROUGH'}

    def disconnect(self,context):
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

        return {'PASS_THROUGH'}
