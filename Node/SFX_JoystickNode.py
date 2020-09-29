import bpy

from .. exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset


class SFX_JoystickNode(bpy.types.Node):
    '''SFX_JoyStick'''
    bl_idname = 'SFX_JoystickNode'
    bl_label = 'Joystick'
    bl_icon = 'AXIS_TOP'
    bl_width_min = 600
    bl_width_max = 5000

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    def update_value(self,context):
        self.update()
        pass

    ww_Joystick_props : bpy.props.PointerProperty(type = SFX_Joystick_Inset)

    actuator_connected_bit1 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False)
    actuator_connected_bit2 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False)
    actuator_name: bpy.props.StringProperty(name = "Actuator Name",
                                    description = "Name of Actuator",
                                    default = "Joystick")    
    socket_ip: bpy.props.StringProperty(name = "Socket ip",
                                    description = "IP of Actuator",
                                    default = "127.0.0.1")
    rsocket_port: bpy.props.StringProperty(name = "Receive Socket port",
                                    description = "Receive Port of Actuator",
                                    default = "15017")
    ssocket_port: bpy.props.StringProperty(name = "Send Socket port",
                                    description = "Send Port of Actuator",
                                    default = "15018")
    operator_started_bit1 : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
                                    default = False)
    TickTime_prop: bpy.props.FloatProperty(name = "Tick Time",
                                    description ="Sanity Check message round trip Time",
                                    default=0.1,
                                    precision=1,
                                    update = update_value)
    expand_Joystick_data : bpy.props.BoolProperty(name = "Joystick Data",
                                    description = "Show Joystick Data",
                                    default = False)

    def init(self, context):

        self.outputs.new('SFX_Joy',name= 'Joy Values')
        self.outputs["Joy Values"].default_value_set = self.ww_Joystick_props

    def copy(self, node):
        print("copied node", node)

    def free(self):
        self.operator_started_bit1 = False
        print('Node destroyed',self)

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
            row7.operator('sfx.joystick',text ='Register')
        else:
           row7.operator('sfx.commstarteddiag',text ='Registered')
        row8.prop(self, 'ssocket_port', text = '')
        row9.prop(self, 'rsocket_port', text = '')
        row10.prop(self, 'socket_ip', text = '')
        row11.prop(self, 'actuator_name', text = '')        

        row2 = layout.row(align=True)
        row2.prop(self, 'expand_Joystick_data')

        if self.expand_Joystick_data:
            self.ww_Joystick_props.draw_Joystick_props(context, layout)

    def draw_buttons_ext(self, context, layout):
        pass

    def update(self):
        try:
            out1 = self.outputs["Joy Values"]
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if out1.is_linked:
                for o in out1.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value.X_Achse        =self.ww_Joystick_props.X_Achse        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Y_Achse        =self.ww_Joystick_props.Y_Achse        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Z_Achse        =self.ww_Joystick_props.Z_Achse        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.X_Rot          =self.ww_Joystick_props.X_Rot          
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Y_Rot          =self.ww_Joystick_props.Y_Rot          
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Z_Rot          =self.ww_Joystick_props.Z_Rot          
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Slider         =self.ww_Joystick_props.Slider         
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button1        =self.ww_Joystick_props.Button1        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button2        =self.ww_Joystick_props.Button2        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button3        =self.ww_Joystick_props.Button3        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button4        =self.ww_Joystick_props.Button4        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button5        =self.ww_Joystick_props.Button5        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button6        =self.ww_Joystick_props.Button6        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button7        =self.ww_Joystick_props.Button7        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button8        =self.ww_Joystick_props.Button8        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button9        =self.ww_Joystick_props.Button9        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button10       =self.ww_Joystick_props.Button10       
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button11       =self.ww_Joystick_props.Button11       
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button12       =self.ww_Joystick_props.Button12 
                        # print(o.to_socket.node.inputs[o.to_socket.name].default_value.Y_Achse)'