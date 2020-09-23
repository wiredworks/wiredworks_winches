import bpy

from mathutils import Vector

from .. exchange_data.ww_Joystick_props import ww_Joystick_props

class JoystickDemux(bpy.types.Node):
    ''' Takes Joystick Data and outputs selected Data'''
    bl_idname = 'ww_JoystickDemuxer'
    bl_label = 'Demuxer'
    bl_icon = 'ARROW_LEFTRIGHT'
    bl_width_min = 220
    bl_width_max = 500

    def update_value(self, context):
        self.update ()
        
    TickTime_prop : bpy.props.FloatProperty(default=0.0, update = update_value)

    Joy_Float     : bpy.props.FloatProperty(default=0.0)

    demux_operator_started_bit1 : bpy.props.BoolProperty(name = "Demux Operator Started",
                                    description = "Demux Operator Started",
                                    default = False)
    demux_operator_running_modal: bpy.props.BoolProperty(name = "Demux Operator Running Modal",
                                    description = "Demux Operator Running Modal",
                                    default = False)

    def init(self, context):
        #self.some_value = 1.2345
        self.outputs.new('ww_Joystick_int_Socket', "Stick")
        self.outputs["Stick"].default_value_set = ww_Joystick_props

        self.outputs.new('ww_Joystick_bool_Socket', "Button 1")
        self.outputs["Button 1"].default_value_set = ww_Joystick_props

        self.outputs.new('ww_Joystick_bool_Socket', "Button 2")
        self.outputs["Button 2"].default_value_set = ww_Joystick_props

        self.inputs.new('ww_Joystick_Socket',name= 'Joy Values')
        self.inputs["Joy Values"].default_value_set = ww_Joystick_props

    def update(self):
        try:
            out1 = self.outputs["Stick"]
            out2 = self.outputs["Button 1"]
            out3 = self.outputs["Button 2"]
            inp2 = self.inputs['Joy Values']
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if inp2.is_linked:
                for i2 in inp2.links:
                    if i2.is_valid:
                        self.outputs["Stick"].default_value.Ptime          = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Ptime          
                        self.outputs["Stick"].default_value.Btimese        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Btime          
                        self.outputs["Stick"].default_value.X_Achse        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.X_Achse
                        self.outputs["Stick"].default_value.Y_Achse        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Y_Achse        
                        self.outputs["Stick"].default_value.Z_Achse        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Z_Achse        
                        self.outputs["Stick"].default_value.X_Rot          = i2.from_socket.node.outputs[i2.from_socket.name].default_value.X_Rot          
                        self.outputs["Stick"].default_value.Y_Rot          = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Y_Rot          
                        self.outputs["Stick"].default_value.Z_Rot          = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Z_Rot          
                        self.outputs["Stick"].default_value.Slider         = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Slider         
                        self.outputs["Stick"].default_value.HAT_Switch     = i2.from_socket.node.outputs[i2.from_socket.name].default_value.HAT_Switch     
                        self.outputs["Stick"].default_value.EndCommOPerator= i2.from_socket.node.outputs[i2.from_socket.name].default_value.EndCommOPerator
                        self.outputs["Stick"].default_value.Destroy        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Destroy        
                        self.outputs["Stick"].default_value.Button1        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button1        
                        self.outputs["Stick"].default_value.Button2        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button2        
                        self.outputs["Stick"].default_value.Button3        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button3        
                        self.outputs["Stick"].default_value.Button4        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button4        
                        self.outputs["Stick"].default_value.Button5        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button5        
                        self.outputs["Stick"].default_value.Button6        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button6        
                        self.outputs["Stick"].default_value.Button7        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button7        
                        self.outputs["Stick"].default_value.Button8        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button8        
                        self.outputs["Stick"].default_value.Button9        = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button9        
                        self.outputs["Stick"].default_value.Button10       = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button10       
                        self.outputs["Stick"].default_value.Button11       = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button11       
                        self.outputs["Stick"].default_value.Button12       = i2.from_socket.node.outputs[i2.from_socket.name].default_value.Button12        
                        #print(self.outputs["Stick"].default_value.X_Achse)
                        pass                                

            if out1.is_linked:
                 for o in out1.links:
                    if o.is_valid:
                        if (self.outputs['Stick'].ww_enum_prop == 'Ptime'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Stick"].default_value.Ptime
                            self.outputs['Stick'].ww_out_value = self.outputs["Stick"].default_value.Ptime
                        elif (self.outputs['Stick'].ww_enum_prop == 'Btime'):
                            o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Stick"].default_value.Btime
                            self.outputs['Stick'].ww_out_value = self.outputs["Stick"].default_value.Btime
                        elif (self.outputs['Stick'].ww_enum_prop == 'X_Achse'):
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

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        box = layout.box()
        col = box.column()
        row4 = col.split(factor=0.75)         # Tick Time
        row5 = row4.split(factor=0.9)       # running modal
        row6 = row5.split(factor=0.9)       # started
        row7 = row6.split(factor=0.5)        # register
        row8 = row7.split(factor=1)           # Joy Float
        row4.prop( self, 'TickTime_prop', text = '')
        row5.prop(self, 'demux_operator_running_modal', text = '')
        row6.prop(self, 'demux_operator_started_bit1', text = '')
        if not(self.demux_operator_started_bit1):
            row7.operator('ww.demux_update',text ='Start')
        else:
            row7.operator('ww.comm_already_started',text ='Started')
        row8.prop(self, 'Joy_Float', text = '') 