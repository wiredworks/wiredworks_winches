import bpy

from .... exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset

from .... exchange_data.sfx import sfx
from .... exchange_data.sfx import sfx_sensor_joystick


class SFX_Joystick_Node(bpy.types.Node):
    '''SFX_JoyStick'''
    bl_idname = 'SFX_Joystick_Node'
    bl_label = 'joystick'
    bl_icon = 'AXIS_TOP'
    bl_width_min = 580
    bl_width_max = 580

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    sfx        : bpy.props.PointerProperty(type = sfx)
    sfx_sensor : bpy.props.PointerProperty(type = sfx_sensor_joystick)

    def init(self, context):
        self.init_sfxData()

        self.outputs.new('SFX_Joy',name= 'Joy Values')
        self.outputs["Joy Values"].default_value_set = sfx.sensors[self.name].Joystick_props

    def copy(self, node):
        print("copied node", node)

    def free(self):
        sfx.sensors[self.name].operator_opened = False
        sfx.sensors.pop(self.name)
        print('Node destroyed',self)

    def draw_buttons(self, context, layout):
        box = layout.box()
        col   = box.column(align = True)
        row4  = col.split(factor=0.85)         # Tick Time
        row5  = row4.split(factor=0.978)       # conn bit1
        row6  = row5.split(factor=0.978)       # conn bit2
        row7  = row6.split(factor=0.978)       # started
        row8  = row7.split(factor=0.978)       # running modal
        row9  = row8.split(factor=0.85)        # label
        row10  = row9.split(factor=0.85)        # ssocket
        row11 = row10.split(factor=0.83)       # rsocket 
        row12 = row11.split(factor=0.5)       # IP
        row13 = row12.split(factor=1)         # Name
        row4.prop(sfx.sensors[self.name], 'TickTime_prop', text = '')
        row5.prop(sfx.sensors[self.name], 'actuator_connected_bit2', text = '')
        row6.prop(sfx.sensors[self.name], 'actuator_connected_bit1', text = '')
        row7.prop(sfx.sensors[self.name], 'operator_running_modal', text = '')
        row8.prop(sfx.sensors[self.name], 'operator_started', text = '')
        if not(sfx.sensors[self.name].operator_started):
            row9.label(text ='Closed')
        else:
           row9.label(text ='Opened')
        row10.prop(sfx.sensors[self.name], 'ssocket_port', text = '')
        row11.prop(sfx.sensors[self.name], 'rsocket_port', text = '')
        row12.prop(sfx.sensors[self.name], 'socket_ip', text = '')
        row13.prop(sfx.sensors[self.name], 'sensor_name', text = '')        

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
            out1 = self.outputs["Joy Values"]
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if out1.is_linked:
                for o in out1.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value.X_Achse        =sfx.sensors[self.name].Joystick_props.X_Achse        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Y_Achse        =sfx.sensors[self.name].Joystick_props.Y_Achse        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Z_Achse        =sfx.sensors[self.name].Joystick_props.Z_Achse        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.X_Rot          =sfx.sensors[self.name].Joystick_props.X_Rot          
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Y_Rot          =sfx.sensors[self.name].Joystick_props.Y_Rot          
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Z_Rot          =sfx.sensors[self.name].Joystick_props.Z_Rot          
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Slider         =sfx.sensors[self.name].Joystick_props.Slider         
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button1        =sfx.sensors[self.name].Joystick_props.Button1        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button2        =sfx.sensors[self.name].Joystick_props.Button2        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button3        =sfx.sensors[self.name].Joystick_props.Button3        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button4        =sfx.sensors[self.name].Joystick_props.Button4        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button5        =sfx.sensors[self.name].Joystick_props.Button5        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button6        =sfx.sensors[self.name].Joystick_props.Button6        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button7        =sfx.sensors[self.name].Joystick_props.Button7        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button8        =sfx.sensors[self.name].Joystick_props.Button8        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button9        =sfx.sensors[self.name].Joystick_props.Button9        
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button10       =sfx.sensors[self.name].Joystick_props.Button10       
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button11       =sfx.sensors[self.name].Joystick_props.Button11       
                        o.to_socket.node.inputs[o.to_socket.name].default_value.Button12       =sfx.sensors[self.name].Joystick_props.Button12 