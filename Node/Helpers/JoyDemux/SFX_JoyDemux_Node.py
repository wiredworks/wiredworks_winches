import bpy

from .... exchange_data.sfx import sfx
from .... exchange_data.sfx import helper_demux
from .... exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset

class SFX_JoyDemux_Node(bpy.types.Node):
    ''' Takes Joystick Data and outputs selected Data'''
    bl_idname = 'SFX_JoyDemux_Node'
    bl_label = 'joydemux'
    bl_icon = 'ANCHOR_LEFT'
    bl_width_min = 220
    bl_width_max = 500

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    # def update_value(self, context):
    #     self.update ()

    # operator_started : bpy.props.BoolProperty(name = "Demux Operator Started",
    #                                 description = "Demux Operator Started",
    #                                 default = False)
    # operator_running_modal: bpy.props.BoolProperty(name = "Demux Operator Running Modal",
    #                                 description = "Demux Operator Running Modal",
    #                                 default = False)
    # operator_restart : bpy.props.BoolProperty(name = "Operator Started",
    #                                 description = "Operator Started",
    #                                 default = False)
        
    # TickTime_prop : bpy.props.FloatProperty(default=0.0,
    #                                         update = update_value)

    sfx              : bpy.props.PointerProperty(type = sfx)
    sfx_helper_demux : bpy.props.PointerProperty(type = helper_demux)

    def init(self, context):
        self.init_sfxData()

        self.outputs.new('SFX_Joy_Float', "Stick")
        self.outputs["Stick"].default_value_set = SFX_Joystick_Inset

        self.outputs.new('SFX_Joy_bool', "Button 1")
        self.outputs["Button 1"].default_value_set = SFX_Joystick_Inset

        self.outputs.new('SFX_Joy_bool', "Button 2")
        self.outputs["Button 2"].default_value_set = SFX_Joystick_Inset
        self.outputs["Button 2"].ww_enum_prop = 'Button6'

        self.inputs.new('SFX_Joy_In',name= 'Joy Values')
        self.inputs["Joy Values"].default_value_set = SFX_Joystick_Inset



    def copy(self, node):
        print("copied node", node)
        
    def free(self):
        sfx.helpers[self.name].operator_started = False
        sfx.helpers.pop(self.name)

    def draw_buttons(self, context, layout):
        box = layout.box()
        col = box.column()
        row4 = col.split(factor=0.75)         # Tick Time
        row5 = row4.split(factor=0.9)         # running modal
        row6 = row5.split(factor=0.9)         # started
        row7 = row6.split(factor=1)           # register
        row4.prop(sfx.helpers[self.name], 'TickTime_prop', text = '')
        row5.prop(sfx.helpers[self.name], 'operator_running_modal', text = '')
        row6.prop(sfx.helpers[self.name], 'operator_started', text = '')
        if not(sfx.helpers[self.name].operator_started):
            row7.operator('sfx.joydemux_op',text ='Start')
        else:
            row7.operator('sfx.commstarteddiag',text ='Started')

    def draw_buttons_ext(self, context, layout):
        pass

    def init_sfxData(self):
        sfx.helpers.update({self.name :self.sfx_helper_demux})
        pass

    def sfx_update(self):
        if sfx.helpers[self.name].operator_running_modal:
            self.color = (0,0.4,0.1)
            self.use_custom_color = True
        else:
            self.use_custom_color = False
        try:
            out1 = self.outputs["Stick"]
            out2 = self.outputs["Button 1"]
            out3 = self.outputs["Button 2"]
            inp1 = self.inputs["Joy Values"]
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if inp1.is_linked:
                for i2 in inp1.links:
                    if i2.is_valid:
                        self.outputs["Stick"].default_value.X_Achse        = self.inputs["Joy Values"].default_value.X_Achse
                        self.outputs["Stick"].default_value.Y_Achse        = self.inputs["Joy Values"].default_value.Y_Achse        
                        self.outputs["Stick"].default_value.Z_Achse        = self.inputs["Joy Values"].default_value.Z_Achse        
                        self.outputs["Stick"].default_value.X_Rot          = self.inputs["Joy Values"].default_value.X_Rot          
                        self.outputs["Stick"].default_value.Y_Rot          = self.inputs["Joy Values"].default_value.Y_Rot          
                        self.outputs["Stick"].default_value.Z_Rot          = self.inputs["Joy Values"].default_value.Z_Rot          
                        self.outputs["Stick"].default_value.Slider         = self.inputs["Joy Values"].default_value.Slider         
                        self.outputs["Stick"].default_value.HAT_Switch     = self.inputs["Joy Values"].default_value.HAT_Switch     
                        self.outputs["Stick"].default_value.Button1        = self.inputs["Joy Values"].default_value.Button1        
                        self.outputs["Stick"].default_value.Button2        = self.inputs["Joy Values"].default_value.Button2        
                        self.outputs["Stick"].default_value.Button3        = self.inputs["Joy Values"].default_value.Button3        
                        self.outputs["Stick"].default_value.Button4        = self.inputs["Joy Values"].default_value.Button4        
                        self.outputs["Stick"].default_value.Button5        = self.inputs["Joy Values"].default_value.Button5        
                        self.outputs["Stick"].default_value.Button6        = self.inputs["Joy Values"].default_value.Button6        
                        self.outputs["Stick"].default_value.Button7        = self.inputs["Joy Values"].default_value.Button7        
                        self.outputs["Stick"].default_value.Button8        = self.inputs["Joy Values"].default_value.Button8        
                        self.outputs["Stick"].default_value.Button9        = self.inputs["Joy Values"].default_value.Button9        
                        self.outputs["Stick"].default_value.Button10       = self.inputs["Joy Values"].default_value.Button10       
                        self.outputs["Stick"].default_value.Button11       = self.inputs["Joy Values"].default_value.Button11       
                        self.outputs["Stick"].default_value.Button12       = self.inputs["Joy Values"].default_value.Button12        

            if out1.is_linked:
                 for o in out1.links:
                    if o.is_valid:
                        if (self.outputs['Stick'].ww_enum_prop == 'X_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Stick"].default_value.X_Achse
                            self.outputs['Stick'].ww_out_value = self.outputs["Stick"].default_value.X_Achse
                        elif (self.outputs['Stick'].ww_enum_prop == 'Y_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Stick"].default_value.Y_Achse
                            self.outputs['Stick'].ww_out_value = self.outputs["Stick"].default_value.Y_Achse
                        elif (self.outputs['Stick'].ww_enum_prop == 'Z_Achse'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Stick"].default_value.Z_Achse
                            self.outputs['Stick'].ww_out_value = self.outputs["Stick"].default_value.Z_Achse
                        elif (self.outputs['Stick'].ww_enum_prop == 'X_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Stick"].default_value.X_Rot
                            self.outputs['Stick'].ww_out_value = self.outputs["Stick"].default_value.X_Rot
                        elif (self.outputs['Stick'].ww_enum_prop == 'Y_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Stick"].default_value.Y_Rot
                            self.outputs['Stick'].ww_out_value = self.outputs["Stick"].default_value.Y_Rot
                        elif (self.outputs['Stick'].ww_enum_prop == 'Z_Rot'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Stick"].default_value.Z_Rot
                            self.outputs['Stick'].ww_out_value = self.outputs["Stick"].default_value.Z_Rot
                        elif (self.outputs['Stick'].ww_enum_prop == 'Slider'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Stick"].default_value.Slider
                            self.outputs['Stick'].ww_out_value = self.outputs["Stick"].default_value.Slider
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = 0.0
            
            if out2.is_linked:
                 for o in out2.links:
                    if o.is_valid:
                        if   (self.outputs['Button 1'].ww_enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button1
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button1
                        elif (self.outputs['Button 1'].ww_enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button2
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button2
                        elif (self.outputs['Button 1'].ww_enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button3
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button3
                        elif (self.outputs['Button 1'].ww_enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button4
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button4
                        elif (self.outputs['Button 1'].ww_enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button5
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button5
                        elif (self.outputs['Button 1'].ww_enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button6
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button6
                        elif (self.outputs['Button 1'].ww_enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button7
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button7
                        elif (self.outputs['Button 1'].ww_enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button8
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button8
                        elif (self.outputs['Button 1'].ww_enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button9
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button9
                        elif (self.outputs['Button 1'].ww_enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button10
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button10
                        elif (self.outputs['Button 1'].ww_enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button11
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button11
                        elif (self.outputs['Button 1'].ww_enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 1"].default_value.Button12
                            self.outputs['Button 1'].ww_out = self.outputs["Stick"].default_value.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False

            if out3.is_linked:
                 for o in out3.links:
                    if o.is_valid:
                        if   (self.outputs['Button 2'].ww_enum_prop == 'Button1'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button1
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button1
                        elif (self.outputs['Button 2'].ww_enum_prop == 'Button2'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button2
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button2
                        elif (self.outputs['Button 2'].ww_enum_prop == 'Button3'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button3
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button3
                        elif (self.outputs['Button 2'].ww_enum_prop == 'Button4'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button4
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button4
                        elif (self.outputs['Button 2'].ww_enum_prop == 'Button5'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button5
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button5
                        elif (self.outputs['Button 2'].ww_enum_prop == 'Button6'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button6
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button6
                        elif (self.outputs['Button 2'].ww_enum_prop == 'Button7'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button7
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button7
                        elif (self.outputs['Button 2'].ww_enum_prop == 'Button8'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button8
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button8
                        elif (self.outputs['Button 2'].ww_enum_prop == 'Button9'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button9
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button9
                        elif (self.outputs['Button 2'].ww_enum_prop == 'Button10'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button10
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button10
                        elif (self.outputs['Button 2'].ww_enum_prop == 'Button11'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button11
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button11
                        elif (self.outputs['Button 2'].ww_enum_prop == 'Button12'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Button 2"].default_value.Button12
                            self.outputs['Button 2'].ww_out = self.outputs["Stick"].default_value.Button12
                        else:
                            o.to_socket.node.inputs[o.to_socket.name].default_value = False


