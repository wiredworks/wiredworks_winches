import bpy

from .. exchange_data.Share import Shared
from .. exchange_data.ww_Joystick_props import ww_Joystick_props


class ww_ActuatorStartCommNode(bpy.types.Node):
    '''ww Starts Comm Operator'''
    bl_idname = 'ww_StartCommOp'
    bl_label = 'Comm Operator'
    bl_icon = 'CURVE_NCIRCLE'
    bl_width_min = 600
    bl_width_max = 5000

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'ww_NodeTree'

    def update_func(self,context):
        #print('k')
        pass

    Shared : bpy.props.PointerProperty(type = Shared,
                                        update = update_func)

    ww_Joystick_props : bpy.props.PointerProperty(type = ww_Joystick_props)

    actuator_connected_bit1 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False,
                                    update = update_func)
    actuator_connected_bit2 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False,
                                    update = update_func)
    actuator_name: bpy.props.StringProperty(name = "Actuator Name",
                                    description = "Name of Actuator",
                                    default = "Joystick"                                    )    
    socket_ip: bpy.props.StringProperty(name = "Socket ip",
                                    description = "IP of Actuator",
                                    default = "127.0.0.1"                                        )
    rsocket_port: bpy.props.StringProperty(name = "Receive Socket port",
                                    description = "Receive Port of Actuator",
                                    default = "15017"                                        )
    ssocket_port: bpy.props.StringProperty(name = "Send Socket port",
                                    description = "Send Port of Actuator",
                                    default = "15018"                                        )
    operator_started_bit1 : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
                                    default = False)
    TickTime_prop: bpy.props.FloatProperty(name = "Tick Time",
                                    description ="Sanity Check message round trip Time",
                                    default=0.1,
                                    precision=1,
                                    update = update_func)
    expand_Joystick_data : bpy.props.BoolProperty(name = "Joystick Data",
                                    description = "Show Joystick Data",
                                    default = False)

    def init(self, context):
        self.draw_model(context)

        output = self.outputs.new('ww_Joystick_output_Socket',name= 'Joy Values')
        output.value_property = ww_Joystick_props
        

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
        box = layout.box()
        col = box.column(align = True)
        row4 = col.split(factor=0.91)         # Tick Time
        row5 = row4.split(factor=0.978)       # conn bit1
        row6 = row5.split(factor=0.978)       # conn bit2
        row7 = row6.split(factor=0.85)        # register
        row8 = row7.split(factor=0.85)        # ssocket
        row9 = row8.split(factor=0.85)        # rsocket 
        row10 = row9.split(factor=0.5)        # IP
        row11 = row10.split(factor=1)         # Name
        row4.prop( self, 'TickTime_prop', text = '')
        row5.prop(self, 'actuator_connected_bit2', text = '')
        row6.prop(self, 'actuator_connected_bit1', text = '')
        if not(self.operator_started_bit1):
            row7.operator('ww.start_comm',text ='Start')
        else:
           row7.operator('ww.comm_already_started',text ='Started')
        row8.prop(self, 'ssocket_port', text = '')
        row9.prop(self, 'rsocket_port', text = '')
        row10.prop(self, 'socket_ip', text = '')
        row11.prop(self, 'actuator_name', text = '')        

        row2 = layout.row(align=True)
        row2.prop(self, 'expand_Joystick_data')

        if self.expand_Joystick_data:
            self.ww_Joystick_props.draw_Joystick_props(context, layout)

        split = layout.split()
        col = split.column()
      
    def draw_buttons_ext(self, context, layout):
        pass

    def draw_model(self,context):

        collection = bpy.data.collections.new('ww SFX_Nodes')
        bpy.context.scene.collection.children.link(collection)