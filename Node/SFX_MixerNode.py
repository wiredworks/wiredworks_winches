import bpy
from .. exchange_data.SFX_actuator_basic_Inset import SFX_actuator_basic_Inset
from .. exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset

class SFX_JoystickDemuxNode(bpy.types.Node):
    ''' Takes two Inputs and mixes them'''
    bl_idname = 'SFX_MixerNode'
    bl_label = 'Mixer'
    bl_icon = 'SNAP_MIDPOINT'
    bl_width_min = 580
    bl_width_max = 580

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    def update_value(self, context):
        self.update ()
        
    TickTime_prop : bpy.props.FloatProperty(default=0.0,
                                            update = update_value)

    Actuator_basic_props : bpy.props.PointerProperty(type =SFX_actuator_basic_Inset)

    expand_Actuator_basic_data : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)

    mixer_operator_started_bit1 : bpy.props.BoolProperty(name = "Mixer Operator Started",
                                    description = "Mixer Operator Started",
                                    default = False)
    mixer_operator_running_modal: bpy.props.BoolProperty(name = "Mixer Operator Running Modal",
                                    description = "Mixer Operator Running Modal",
                                    default = False)

    factor : bpy.props.FloatProperty(name='Factor',
                                      description='Factor',
                                      default = 50.0,
                                      soft_max = 100.0,
                                      soft_min = 0.0)

    def init(self, context):
        self.outputs.new('SFX_Cue_Float', "Set Vel")
        self.outputs["Set Vel"].default_value_set = SFX_Joystick_Inset
        self.outputs["Set Vel"].ww_out_value = 0.0

        self.inputs.new('SFX_act_in_set_Vel',name= 'Channel 1')
        self.inputs["Channel 1"].set_vel = 0.0

        self.inputs.new('SFX_act_in_set_Vel',name= 'Channel 2')
        self.inputs["Channel 2"].set_vel = 0.0
        pass
    def copy(self, node):
        print("copied node", node)
        
    def free(self):
        self.MotherNode.demux_operator_started_bit1 = False

    def update(self):
        #print('update')
        try:
            out1 = self.outputs["Set Vel"]
            inp1 = self.inputs["Channel 1"]
            inp2 = self.inputs["Channel 2"]
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if inp1.is_linked:
                for i1 in inp1.links:
                    if i1.is_valid:
                        self.inputs["Channel 1"].set_vel=i1.from_socket.node.outputs[i1.from_socket.name].ww_out_value
                        # self.Actuator_basic_props.soll_Vel = \
                        #    (self.inputs["Channel 1"].set_vel * self.Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop)/100.0  
                        pass
            if inp2.is_linked:
                for i2 in inp2.links:
                    if i2.is_valid:
                        self.inputs["Channel 2"].set_vel=i2.from_socket.node.outputs[i2.from_socket.name].ww_out_value
                        # self.Actuator_basic_props.soll_Vel = \
                        #    (self.inputs["Channel 2"].set_vel * self.Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop)/100.0  
                        pass            
            if out1.is_linked:
                 for o in out1.links:
                    if o.is_valid:
                        self.outputs["Set Vel"].ww_out_value = (self.inputs["Channel 1"].set_vel*(self.factor/100.0)+self.inputs["Channel 2"].set_vel*(1.0-self.factor/100.0))
                        o.to_socket.node.inputs[o.to_socket.name].set_vel = self.outputs["Set Vel"].ww_out_value
                        self.Actuator_basic_props.diff_Vel                                     = o.to_socket.node.Actuator_basic_props.diff_Vel
                        self.Actuator_basic_props.soll_Vel                                     = o.to_socket.node.Actuator_basic_props.soll_Vel
                        self.Actuator_basic_props.ist_Pos                                      = o.to_socket.node.Actuator_basic_props.ist_Pos
                        self.Actuator_basic_props.ist_Force                                    = o.to_socket.node.Actuator_basic_props.ist_Force
                        self.Actuator_basic_props.ist_Vel                                      = o.to_socket.node.Actuator_basic_props.ist_Vel
                        self.Actuator_basic_props.enable_Actuator                              = o.to_socket.node.Actuator_basic_props.enable_Actuator
                        self.Actuator_basic_props.select_Actuator                              = o.to_socket.node.Actuator_basic_props.select_Actuator
                        self.Actuator_basic_props.online_Actuator                              = o.to_socket.node.Actuator_basic_props.online_Actuator
                        self.Actuator_basic_props.Status                                       = o.to_socket.node.Actuator_basic_props.Status
                        self.AcStuator_basic_props.Actuator_props.simple_actuator_HardMax_prop = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
                        self.Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop  = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
                        self.Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop   = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop
                        self.Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop   = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop
                        self.Actuator_basic_props.Actuator_props.simple_actuator_confirm       = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_confirm
                        self.Actuator_basic_props.Actuator_props.simple_actuator_confirmed     = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_confirmed
                        self.Actuator_basic_props.DigTwin_basic_props.start_Loc                = o.to_socket.node.Actuator_basic_props.DigTwin_basic_props.start_Loc
                        self.Actuator_basic_props.DigTwin_basic_props.con_Loc                  = o.to_socket.node.Actuator_basic_props.DigTwin_basic_props.con_Loc
                        self.Actuator_basic_props.DigTwin_basic_props.end_Loc                  = o.to_socket.node.Actuator_basic_props.DigTwin_basic_props.end_Loc
                        self.Actuator_basic_props.DigTwin_basic_props.length                   = o.to_socket.node.Actuator_basic_props.DigTwin_basic_props.length
                        self.Actuator_basic_props.DigTwin_basic_props.mass_column1             = o.to_socket.node.Actuator_basic_props.DigTwin_basic_props.mass_column1
                        self.Actuator_basic_props.DigTwin_basic_props.mass_column2             = o.to_socket.node.Actuator_basic_props.DigTwin_basic_props.mass_column2
                        self.Actuator_basic_props.DigTwin_basic_props.mass_column3             = o.to_socket.node.Actuator_basic_props.DigTwin_basic_props.mass_column3
                        self.Actuator_basic_props.DigTwin_basic_props.y_z_scale                = o.to_socket.node.Actuator_basic_props.DigTwin_basic_props.y_z_scale
                        pass
 
    def draw_buttons(self, context, layout):
        split = layout.split(factor=0.65)
        col = split.column()


        col1 = split.column()
        box = col1.box()
        col = box.column()
        row4 = col.split(factor=0.75)         # Tick Time
        row5 = row4.split(factor=0.9)       # running modal
        row6 = row5.split(factor=0.9)       # started
        row7 = row6.split(factor=1)        # register
        row4.prop( self, 'TickTime_prop', text = '')
        row5.prop(self, 'mixer_operator_running_modal', text = '')
        row6.prop(self, 'mixer_operator_started_bit1', text = '')
        if not(self.mixer_operator_started_bit1):
            row7.operator('sfx.mixerop',text ='Start')
        else:
            row7.operator('sfx.commstarteddiag',text ='Started')

        box = layout.box()
        col = box.column()
        row = col.split(factor=0.9)
        row1 = row.split(factor=0.1)
        row2 = row1.split(factor=1)
        row.label(text='Input 1')
        row1.prop(self,'factor',text='',slider = True)
        row2.label(text='Input 2')   

        row2 = layout.row(align=True)
        row2.prop(self, 'expand_Actuator_basic_data')
        if self.expand_Actuator_basic_data:
            self.Actuator_basic_props.draw_Actuator_basic_props(context, layout)

