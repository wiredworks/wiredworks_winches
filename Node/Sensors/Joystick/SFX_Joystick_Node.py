import bpy

from .... exchange_data.sfx import sfx

from .SFX_Joystick_Data import sensor_joystick
from .SFX_Joystick_Inset import SFX_Joystick_Inset

class SFX_Joystick_Node(bpy.types.Node):
    '''SFX_JoyStick'''
    bl_idname = 'SFX_Joystick_Node'
    bl_label = 'joystick'
    bl_icon = 'AXIS_TOP'
    bl_width_min = 180
    bl_width_max = 180

    sfx_type     = 'Sensor'
    sfx_sub_type = 'HID'
    sfx_id       = 'joystick'

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    sfx        : bpy.props.PointerProperty(type = sfx)
    sfx_sensor : bpy.props.PointerProperty(type = sensor_joystick)

    def init(self, context):
        self.init_sfxData()

        self.outputs.new('SFX_JoyDemux_Socket_Float', "Float-1").hide
        self.outputs["Float-1"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Float', "Float-2").hide = True
        self.outputs["Float-2"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Float', "Float-3").hide = True
        self.outputs["Float-3"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Float', "Float-4").hide = True
        self.outputs["Float-4"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Float', "Float-5").hide = True
        self.outputs["Float-5"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Float', "Float-6").hide = True
        self.outputs["Float-6"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Float', "Float-7").hide = True
        self.outputs["Float-7"].default_value_set = SFX_Joystick_Inset

        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 1")
        self.outputs["Button 1"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 2").hide = True
        self.outputs["Button 2"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 3").hide = True
        self.outputs["Button 3"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 4").hide = True
        self.outputs["Button 4"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 5").hide = True
        self.outputs["Button 5"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 6").hide = True
        self.outputs["Button 6"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 7").hide = True
        self.outputs["Button 7"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 8").hide = True
        self.outputs["Button 8"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 9").hide = True
        self.outputs["Button 9"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 10").hide = True
        self.outputs["Button 10"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 11").hide = True
        self.outputs["Button 11"].default_value_set = SFX_Joystick_Inset
        self.outputs.new('SFX_JoyDemux_Socket_Bool', "Button 12").hide = True
        self.outputs["Button 12"].default_value_set = SFX_Joystick_Inset

    def copy(self, node):
        print("copied node", node)

    def free(self):
        sfx.sensors[self.name].operator_opened = False
        sfx.sensors.pop(self.name)
        print('Node destroyed',self)

    def draw_buttons(self, context, layout):
        try:
            sfx.sensors[self.name]
        except KeyError:
            self.init_sfxData()
        box = layout.box()
        boxA = box.box()
        boxC = boxA.box()    
        col1 = boxC.column()
        row = col1.row()
        row.separator(factor = 1) 
        row.separator(factor = 1)        
        row.prop(sfx.sensors[self.name], 'TickTime_prop', text = '')
        row.separator(factor = 1)
        row.separator(factor = 1) 
        row = col1.row()
        row.separator(factor = 1) 
        row.separator(factor = 1)
        row.separator(factor = 1)
        row.prop(sfx.sensors[self.name], 'actuator_connected_bit1', text = '') 
        row.prop(sfx.sensors[self.name], 'actuator_connected_bit2', text = '')
        boxB = boxA.box()
        col2 = boxB.column()
        row = col2.row()
        row.prop(sfx.sensors[self.name], 'sensor_name', text = '')
        row = col2.row()
        row.separator(factor = 1)
        row.separator(factor = 1) 
        row.separator(factor = 1)      
        row.prop(sfx.sensors[self.name], 'ssocket_port', text = '')
        row.separator(factor = 1)
        row.separator(factor = 1)
        row.separator(factor = 1)
        row = col2.row()
        row.separator(factor = 1)
        row.separator(factor = 1)
        row.separator(factor = 1)         
        row.prop(sfx.sensors[self.name], 'rsocket_port', text = '')
        row.separator(factor = 1)
        row.separator(factor = 1)
        row.separator(factor = 1) 
        col2.prop(sfx.sensors[self.name], 'socket_ip', text = '')
        row = col2.row()
        row.separator(factor = 1)
        row.separator(factor = 1) 
        row.separator(factor = 1)
        row.prop(sfx.sensors[self.name], 'operator_started', text = '')
        row.prop(sfx.sensors[self.name], 'operator_running_modal', text = '')
        row = col2.row()
        row.separator(factor = 1)
        row.separator(factor = 1) 
        row.separator(factor = 1) 
        if not(sfx.sensors[self.name].operator_started):
            row.label(text ='Closed')
        else:
            row.label(text ='Opened')

        row2 = layout.row(align=True)
        row2.prop(sfx.sensors[self.name], 'expand_Joystick_data')

        if sfx.sensors[self.name].expand_Joystick_data:
            sfx.sensors[self.name].Joystick_props.draw_Joystick_props(context, layout)

    def draw_buttons_ext(self, context, layout):
        pass

    def init_sfxData(self):
        sfx.sensors.update({self.name :self.sfx_sensor})
        pass

    def sfx_update(self):
        if sfx.sensors[self.name].operator_running_modal:
            self.color = (0,0.4,0.1)
            self.use_custom_color = True
        else:
            self.use_custom_color = False
        try:
            out1 =self.outputs["Float-1"]
            out2 =self.outputs["Float-2"]
            out3 =self.outputs["Float-3"]
            out4 =self.outputs["Float-4"]
            out5 =self.outputs["Float-5"]
            out6 =self.outputs["Float-6"]
            out7 =self.outputs["Float-7"]

            out8 =self.outputs["Button 1"]
            out9 =self.outputs["Button 2"]
            out10 =self.outputs["Button 3"]
            out11 =self.outputs["Button 4"]
            out12 =self.outputs["Button 5"]
            out13 =self.outputs["Button 6"]
            out14 =self.outputs["Button 7"]
            out15 =self.outputs["Button 8"]
            out16 =self.outputs["Button 9"]
            out17 =self.outputs["Button 10"]
            out18 =self.outputs["Button 11"]
            out19 =self.outputs["Button 12"]

            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if out1.is_linked:
                out2.hide = False
                for o in out1.links:
                    if o.is_valid:
                        if (out1.enum_prop == 'X_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Achse
                            out1.float = sfx.sensors[self.name].Joystick_props.X_Achse
                        elif (out1.enum_prop == 'Y_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Achse
                            out1.float = sfx.sensors[self.name].Joystick_props.Y_Achse
                        elif (out1.enum_prop == 'Z_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Achse
                            out1.float = sfx.sensors[self.name].Joystick_props.Z_Achse
                        elif (out1.enum_prop == 'X_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Rot
                            out1.float = sfx.sensors[self.name].Joystick_props.X_Rot
                        elif (out1.enum_prop == 'Y_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Rot
                            out1.float = sfx.sensors[self.name].Joystick_props.Y_Rot
                        elif (out1.enum_prop == 'Z_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Rot
                            out1.float = sfx.sensors[self.name].Joystick_props.Z_Rot
                        elif (out1.enum_prop == 'Slider'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Slider
                            out1.float = sfx.sensors[self.name].Joystick_props.Slider
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = 0.0
            else:
                out2.hide = True
            if out2.is_linked:
                out3.hide = False
                for o in out2.links:
                    if o.is_valid:
                        if (out2.enum_prop == 'X_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Achse
                            out2.float = sfx.sensors[self.name].Joystick_props.X_Achse
                        elif (out2.enum_prop == 'Y_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Achse
                            out2.float = sfx.sensors[self.name].Joystick_props.Y_Achse
                        elif (out2.enum_prop == 'Z_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Achse
                            out2.float = sfx.sensors[self.name].Joystick_props.Z_Achse
                        elif (out2.enum_prop == 'X_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Rot
                            out2.float = sfx.sensors[self.name].Joystick_props.X_Rot
                        elif (out2.enum_prop == 'Y_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Rot
                            out2.float = sfx.sensors[self.name].Joystick_props.Y_Rot
                        elif (out2.enum_prop == 'Z_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Rot
                            out2.float = sfx.sensors[self.name].Joystick_props.Z_Rot
                        elif (out2.enum_prop == 'Slider'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Slider
                            out2.float = sfx.sensors[self.name].Joystick_props.Slider
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = 0.0
            else:
                out3.hide = True
            if out3.is_linked:
                out4.hide = False
                for o in out3.links:
                    if o.is_valid:
                        if (out3.enum_prop == 'X_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Achse
                            out3.float = sfx.sensors[self.name].Joystick_props.X_Achse
                        elif (out3.enum_prop == 'Y_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Achse
                            out3.float = sfx.sensors[self.name].Joystick_props.Y_Achse
                        elif (out3.enum_prop == 'Z_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Achse
                            out3.float = sfx.sensors[self.name].Joystick_props.Z_Achse
                        elif (out3.enum_prop == 'X_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Rot
                            out3.float = sfx.sensors[self.name].Joystick_props.X_Rot
                        elif (out3.enum_prop == 'Y_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Rot
                            out3.float = sfx.sensors[self.name].Joystick_props.Y_Rot
                        elif (out3.enum_prop == 'Z_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Rot
                            out3.float = sfx.sensors[self.name].Joystick_props.Z_Rot
                        elif (out3.enum_prop == 'Slider'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Slider
                            out3.float = sfx.sensors[self.name].Joystick_props.Slider
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = 0.0
            else:
                out4.hide = True
            if out4.is_linked:
                out5.hide = False
                for o in out4.links:
                    if o.is_valid:
                        if (out4.enum_prop == 'X_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Achse
                            out4.float = sfx.sensors[self.name].Joystick_props.X_Achse
                        elif (out4.enum_prop == 'Y_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Achse
                            out4.float = sfx.sensors[self.name].Joystick_props.Y_Achse
                        elif (out4.enum_prop == 'Z_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Achse
                            out4.float = sfx.sensors[self.name].Joystick_props.Z_Achse
                        elif (out3.enum_prop == 'X_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Rot
                            out4.float = sfx.sensors[self.name].Joystick_props.X_Rot
                        elif (out4.enum_prop == 'Y_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Rot
                            out4.float = sfx.sensors[self.name].Joystick_props.Y_Rot
                        elif (out4.enum_prop == 'Z_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Rot
                            out4.float = sfx.sensors[self.name].Joystick_props.Z_Rot
                        elif (out4.enum_prop == 'Slider'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Slider
                            out4.float = sfx.sensors[self.name].Joystick_props.Slider
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = 0.0
            else:
                out5.hide = True
            if out5.is_linked:
                out6.hide = False
                for o in out5.links:
                    if o.is_valid:
                        if (out5.enum_prop == 'X_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Achse
                            out5.float = sfx.sensors[self.name].Joystick_props.X_Achse
                        elif (out5.enum_prop == 'Y_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Achse
                            out5.float = sfx.sensors[self.name].Joystick_props.Y_Achse
                        elif (out5.enum_prop == 'Z_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Achse
                            out5.float = sfx.sensors[self.name].Joystick_props.Z_Achse
                        elif (out5.enum_prop == 'X_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Rot
                            out5.float = sfx.sensors[self.name].Joystick_props.X_Rot
                        elif (out5.enum_prop == 'Y_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Rot
                            out5.float = sfx.sensors[self.name].Joystick_props.Y_Rot
                        elif (out5.enum_prop == 'Z_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Rot
                            out5.float = sfx.sensors[self.name].Joystick_props.Z_Rot
                        elif (out5.enum_prop == 'Slider'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Slider
                            out5.float = sfx.sensors[self.name].Joystick_props.Slider
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = 0.0
            else:
                out6.hide = True
            if out6.is_linked:
                out7.hide = False
                for o in out6.links:
                    if o.is_valid:
                        if (out6.enum_prop == 'X_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Achse
                            out6.float = sfx.sensors[self.name].Joystick_props.X_Achse
                        elif (out6.enum_prop == 'Y_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Achse
                            out6.float = sfx.sensors[self.name].Joystick_props.Y_Achse
                        elif (out6.enum_prop == 'Z_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Achse
                            out6.float = sfx.sensors[self.name].Joystick_props.Z_Achse
                        elif (out6.enum_prop == 'X_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Rot
                            out6.float = sfx.sensors[self.name].Joystick_props.X_Rot
                        elif (out6.enum_prop == 'Y_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Rot
                            out6.float = sfx.sensors[self.name].Joystick_props.Y_Rot
                        elif (out6.enum_prop == 'Z_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Rot
                            out6.float = sfx.sensors[self.name].Joystick_props.Z_Rot
                        elif (out6.enum_prop == 'Slider'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Slider
                            out6.float = sfx.sensors[self.name].Joystick_props.Slider
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = 0.0
            else:
                out7.hide = True
                for o in out7.links:
                    if o.is_valid:
                        if (out7.enum_prop == 'X_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Achse
                            out7.float = sfx.sensors[self.name].Joystick_props.X_Achse
                        elif (out7.enum_prop == 'Y_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Achse
                            out7.float = sfx.sensors[self.name].Joystick_props.Y_Achse
                        elif (out7.enum_prop == 'Z_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Achse
                            out7.float = sfx.sensors[self.name].Joystick_props.Z_Achse
                        elif (out7.enum_prop == 'X_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.X_Rot
                            out7.float = sfx.sensors[self.name].Joystick_props.X_Rot
                        elif (out7.enum_prop == 'Y_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Y_Rot
                            out7.float = sfx.sensors[self.name].Joystick_props.Y_Rot
                        elif (out7.enum_prop == 'Z_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Z_Rot
                            out7.float = sfx.sensors[self.name].Joystick_props.Z_Rot
                        elif (out7.enum_prop == 'Slider'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Slider
                            out7.float = sfx.sensors[self.name].Joystick_props.Slider
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = 0.0

            if out8.is_linked:
                out9.hide = False
                for o in out8.links:
                    if o.is_valid:
                        if   (out8.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out8.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out8.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out8.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out8.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out8.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out8.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out8.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out8.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out8.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out8.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out8.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out8.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False

            else:
                out9.hide = True
            if out9.is_linked:
                out10.hide = False
                for o in out9.links:
                    if o.is_valid:
                        if   (out9.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out9.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out9.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out9.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out9.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out9.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out9.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out9.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out9.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out9.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out9.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out9.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out9.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False
            else:
                out10.hide = True
            if out10.is_linked:
                out11.hide = False
                for o in out10.links:
                    if o.is_valid:
                        if   (out10.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out10.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out10.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out10.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out10.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out10.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out10.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out10.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out10.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out10.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out10.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out10.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out10.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False
            else:
                out11.hide = True
            if out11.is_linked:
                out12.hide = False
                for o in out11.links:
                    if o.is_valid:
                        if   (out11.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out11.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out11.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out11.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out11.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out11.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out11.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out11.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out11.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out11.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out11.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out11.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out11.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False
            else:
                out12.hide = True
            if out12.is_linked:
                out13.hide = False
                for o in out12.links:
                    if o.is_valid:
                        if   (out12.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out12.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out12.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out12.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out12.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out12.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out12.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out12.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out12.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out12.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out12.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out12.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out12.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False
            else:
                out13.hide = True
            if out13.is_linked:
                out14.hide = False
                for o in out13.links:
                    if o.is_valid:
                        if   (out13.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out13.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out13.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out13.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out13.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out13.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out13.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out13.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out13.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out13.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out13.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out13.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out13.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False
            else:
                out14.hide = True
            if out14.is_linked:
                out15.hide = False
                for o in out14.links:
                    if o.is_valid:
                        if   (out14.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out14.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out14.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out14.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out14.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out14.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out14.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out14.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out14.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out14.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out14.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out14.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out14.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False
            else:
                out15.hide = True
            if out15.is_linked:
                out16.hide = False
                for o in out15.links:
                    if o.is_valid:
                        if   (out15.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out15.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out15.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out15.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out15.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out15.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out15.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out15.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out15.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out15.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out15.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out15.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out15.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False
            else:
                out16.hide = True
            if out16.is_linked:
                out17.hide = False
                for o in out16.links:
                    if o.is_valid:
                        if   (out16.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out16.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out16.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out16.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out16.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out16.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out16.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out16.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out16.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out16.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out16.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out16.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out16.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False
            else:
                out17.hide = True
            if out17.is_linked:
                out18.hide = False
                for o in out17.links:
                    if o.is_valid:
                        if   (out17.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out17.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out17.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out17.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out17.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out17.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out17.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out17.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out17.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out17.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out17.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out17.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out17.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False
            else:
                out18.hide = True
            if out18.is_linked:
                out19.hide = False
                for o in out18.links:
                    if o.is_valid:
                        if   (out18.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out18.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out18.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out18.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out18.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out18.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out18.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out18.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out18.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out18.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out18.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out18.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out18.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False
            else:
                out19.hide = True
            if out19.is_linked:
                for o in out19.links:
                    if o.is_valid:
                        if   (out19.enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button1
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button1
                        elif (out19.enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button2
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button2
                        elif (out19.enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button3
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button3
                        elif (out19.enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button4
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button4
                        elif (out19.enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button5
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button5
                        elif (out19.enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button6
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button6
                        elif (out19.enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button7
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button7
                        elif (out19.enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button8
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button8
                        elif (out19.enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button9
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button9
                        elif (out19.enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button10
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button10
                        elif (out19.enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button11
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button11
                        elif (out19.enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = sfx.sensors[self.name].Joystick_props.Button12
                            out19.bool = sfx.sensors[self.name].Joystick_props.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False

