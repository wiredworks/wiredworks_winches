import bpy

from .. exchange_data.Share import Shared


class ww_ActuatorStartCommNode(bpy.types.Node):
    '''ww Starts Comm Operator'''
    bl_idname = 'ww_StartCommOp'
    bl_label = 'Comm Operator'
    bl_icon = 'CURVE_NCIRCLE'
    bl_width_min = 160
    bl_width_max = 160

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'ww_NodeTree'

    def update_func(self,context):
        #print('k')
        #print(Shared)
        pass

    Shared : bpy.props.PointerProperty(type = Shared,
                                        update = update_func)

    soll_Pos : bpy.props.FloatProperty(name = "Soll Pos",
                                    description = "Soll Position",
                                    precision = 3,
                                    default = 0.001,
                                    update = update_func)
    ist_Pos : bpy.props.FloatProperty(name = "Ist Pos",
                                    description = "Ist Position",
                                    precision = 3,
                                    default = 0.001,
                                    update = update_func)
    soll_Vel : bpy.props.FloatProperty(name = "Soll Vel",
                                    description = "Soll Velocity",
                                    precision = 3,
                                    default = 0.001,
                                    update = update_func)
    ist_Vel : bpy.props.FloatProperty(name = "Ist Vel",
                                    description = "Ist Velocity",
                                    precision = 3,
                                    default = 0.001,
                                    update = update_func)
    actuator_connected_bit1 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False,
                                    update = update_func)
    actuator_connected_bit2 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False,
                                    update = update_func)
    cycle_time : bpy.props.FloatProperty(name = "Cycle Time",
                                    description = "Round Trip Time",
                                    precision = 3,
                                    default = 0.001,
                                    update = update_func)
    actuator_name: bpy.props.StringProperty(name = "Actuator Name",
                                        description = "Name of Actuator",
                                        default = "Anton",
                                        )    
    socket_ip: bpy.props.StringProperty(name = "Socket ip",
                                        description = "IP of Actuator",
                                        default = "127.0.0.1",
                                        )
    rsocket_port: bpy.props.StringProperty(name = "Receive Socket port",
                                        description = "Receive Port of Actuator",
                                        default = "15019",
                                        )
    ssocket_port: bpy.props.StringProperty(name = "Send Socket port",
                                        description = "Send Port of Actuator",
                                        default = "15020",
                                        )
    operator_started_bit1 : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
                                    default = False)
    def init(self, context):
        pass

    def copy(self, node):
        print("copied node", node)

    def free(self):
        ID = (self.actuator_name+'_'+
              str(self.socket_ip)+'_'+
              str(self.rsocket_port)+'_'+
              str(self.ssocket_port))
        print("NODE")
        print(ID)
        print(self.Shared.ww_data)
        self.Shared.ww_data[ID]["Destroy"] = True
        print("Node removed", ID, self)

    def draw_buttons(self, context, layout):
        split = layout.split()
        col = split.column()
        if not(self.operator_started_bit1):
            col.operator('ww.start_comm',text ='Start')
        else:
           col.operator('ww.comm_already_started',text ='Started')
      
    def draw_buttons_ext(self, context, layout):
        pass
