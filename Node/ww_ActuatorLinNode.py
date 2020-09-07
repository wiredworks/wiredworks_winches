import bpy
import time
import ctypes

VK_ESCAPE =0x1B

class Shared(bpy.types.PropertyGroup):
    bl_idname = 'ww_Share'

    ww_base_data = { "Ptime"  : 0,
                "Btime"  : 0,
                "X-Soll" : -1.0 ,
                "Y-Soll" : -1.0,
                "Z-Soll" : -1,
                "X-Ist"  : 0.0,
                "Y-Ist"  : 0.0,
                "Z-Ist"  : 0.0,
                "Destroy": False}

    ww_data = {"Name_IP_RPort_SPort": ww_base_data}

    def add_actuator(self,actuator):

        print(actuator.actuator_name,
              actuator.socket_ip,
              actuator.rsocket_port,
              actuator.ssocket_port)

        ID = (actuator.actuator_name+'_'+
              str(actuator.socket_ip)+'_'+
              str(actuator.rsocket_port)+'_'+
              str(actuator.ssocket_port))

        self.ww_data[ID] = self.ww_base_data

class ww_ActuatorLinNode(bpy.types.Node):
    '''ww Linear Actuator'''
    bl_idname = 'ww_ActuatorLin'
    bl_label = 'Lin Actuator'
    bl_icon = 'ARROW_LEFTRIGHT'
    bl_width_min = 400
    bl_width_max = 5000

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
    rsocket_port: bpy.props.StringProperty(name = "Socket port",
                                        description = "Port of Actuator",
                                        default = "15021",
                                        )
    ssocket_port: bpy.props.StringProperty(name = "Socket port",
                                        description = "Port of Actuator",
                                        default = "15022",
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
        #print(dir(self))
        #print(self.operator_started_bit1)
        box = layout.box()
        col = box.column(align = True)
        row1 = col.split(factor=0.86)
        row2 = row1.split(factor=0.95)
        row3 = row2.split(factor=0.95)
        row4 = row3.split(factor=0.82)
        row5 = row4.split(factor=0.75)
        row6 = row5.split(factor=0.3)
        row7 = row6.split(factor=1)
        row1.prop(self, 'cycle_time', text = '')
        row2.prop(self, 'actuator_connected_bit2', text = '')
        row3.prop(self, 'actuator_connected_bit1', text = '')
        row4.prop(self, 'ssocket_port', text = '')
        row5.prop(self, 'rsocket_port', text = '')
        row6.prop(self, 'socket_ip', text = '')
        row7.prop(self, 'actuator_name', text = '')

        row = layout.row()
        split = layout.split()
        col = split.column()
        col.label(text='Soll Pos')        
        col.prop(self, 'soll_Pos' , text = '')
        col = split.column()
        col.label(text='Ist Pos')
        col.prop(self, 'ist_Pos' , text = '')
        col = split.column()
        col.label(text='Soll Vel')
        col.prop(self, 'soll_Vel' , text = '')
        col = split.column()
        col.label(text='Ist Vel')
        col.prop(self, 'ist_Vel' , text = '')
        col = split.column()
        if not(self.operator_started_bit1):
            col.operator('ww.actuator_connect',text ='Start')
        else:
           col.operator('ww.connector_already_started',text ='Started')
        col.operator('ww.actuator_enable',text ='Enable')
        #print(Shared.ww_data['X-Soll'])
 
    def draw_buttons_ext(self, context, layout):
        layout.label(text='Adress')
        layout.prop(self, 'socket_ip', text = 'IP')
        layout.prop(self, 'rsocket_port', text = 'Rec Port')
        layout.prop(self, 'ssocket_port', text = 'Send Port')



    #OPTIONAL
    #we can use this function to dynamically define the label of
    #   the node, however defining the bl_label explicitly overrides it
    #def draw_label(self):
    #   return "this label is shown"

