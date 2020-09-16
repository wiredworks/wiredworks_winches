import bpy

from mathutils import Vector

from .. exchange_data.ww_Joystick_props import ww_Joystick_props

class JoystickDemux(bpy.types.Node):
    ''' Takes Joustick Data and outputs selected Data'''
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
        self.some_value = 1.2345
        self.outputs.new('NodeSocketFloat', "Float")
        self.outputs["Float"].default_value = self.TickTime_prop

        self.inputs.new('NodeSocketFloat',name= 'Joy Float')
        self.inputs["Joy Float"].default_value = self.TickTime_prop

        self.inputs.new('ww_Joystick_Socket',name= 'Joy Values')
        self.inputs["Joy Values"].default_value_set = ww_Joystick_props

    def update(self):
        try:
            out = self.outputs["Float"]
            inp1 = self.inputs['Joy Float']
            inp2 = self.inputs['Joy Values']
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if inp1.is_linked:
                for i1 in inp1.links:
                    if i1.is_valid:
                        self.Joy_Float=i1.from_socket.node.outputs[i1.from_socket.name].default_value

            if inp2.is_linked:
                #print('input linked')
                for i2 in inp2.links:
                    #print(('#####'))
                    if i2.is_valid:
                        #print('input valid')
                        print(i2.from_socket.node.outputs[i2.from_socket.name].default_value)
                        pass                                

            # if out.is_linked:
            #     # I am an ouput node that is linked, try to update my link.
            #     for o in out.links:
            #         if o.is_valid:
            #             o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Float"].default_value   #self.some_value

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