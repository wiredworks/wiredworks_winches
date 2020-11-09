import bpy

from .... exchange_data.sfx import sfx
from .... exchange_data.sfx import SFX_Joystick_Inset

from .SFX_Mixer_Data import helper_mixer

class SFX_Mixer_Node(bpy.types.Node):
    ''' Takes two Inputs and mixes them'''
    bl_idname = 'SFX_Mixer_Node'
    bl_label = 'mixer'
    bl_icon = 'SNAP_MIDPOINT'
    bl_width_min = 580
    bl_width_max = 580

    sfx_type = 'Helper'

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    sfx              : bpy.props.PointerProperty(type = sfx)
    sfx_helper_mixer : bpy.props.PointerProperty(type = helper_mixer)

    def init(self, context):
        self.init_sfxData()

        self.outputs.new('SFX_Socket_Float', "Set Vel")
        self.outputs["Set Vel"].float = 0.0

        self.inputs.new('SFX_Socket_Float',name= 'Channel 1')
        self.inputs["Channel 1"].float = 0.0

        self.inputs.new('SFX_Socket_Float',name= 'Channel 2')
        self.inputs["Channel 2"].float = 0.0

    def copy(self, node):
        print("copied node", node)
        
    def free(self):
        sfx.helpers[self.name].operator_started = False
        sfx.helpers.pop(self.name)

    def draw_buttons(self, context, layout):
        try:
            sfx.sensors[self.name]
        except KeyError:
            self.init_sfxData()
        split = layout.split(factor=0.65)
        col = split.column()
        col1 = split.column()
        box = col1.box()
        col = box.column()
        row4 = col.split(factor=0.75)         # Tick Time
        row5 = row4.split(factor=0.9)       # running modal
        row6 = row5.split(factor=0.9)       # started
        row7 = row6.split(factor=1)        # register
        row4.prop(sfx.helpers[self.name], 'TickTime_prop', text = '')
        row5.prop(sfx.helpers[self.name], 'operator_running_modal', text = '')
        row6.prop(sfx.helpers[self.name], 'operator_started', text = '')
        if not(sfx.helpers[self.name].operator_started):
            row7.label(text ='Stoped')
        else:
            row7.label(text ='Started')

        box = layout.box()
        col = box.column()
        row = col.split(factor=0.9)
        row1 = row.split(factor=0.1)
        row2 = row1.split(factor=1)
        row.label(text='Input 1')
        row1.prop(sfx.helpers[self.name],'factor',text='',slider = True)
        row2.label(text='Input 2')   

        row2 = layout.row(align=True)
        row2.prop(sfx.helpers[self.name], 'expand_Actuator_basic_data')
        if sfx.helpers[self.name].expand_Actuator_basic_data:
            sfx.helpers[self.name].Actuator_basic_props.draw_Actuator_basic_props(context, layout)

    def draw_buttons_ext(self, context, layout):
        pass

    def init_sfxData(self):
        sfx.helpers.update({self.name :self.sfx_helper_mixer})

    def sfx_update(self):
        if sfx.helpers[self.name].operator_running_modal:
            self.color = (0,0.4,0.1)
            self.use_custom_color = True
        else:
            self.use_custom_color = False
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
                        self.inputs["Channel 1"].float=i1.from_socket.node.outputs[i1.from_socket.name].float
                        pass
            if inp2.is_linked:
                for i2 in inp2.links:
                    if i2.is_valid:
                        self.inputs["Channel 2"].float=i2.from_socket.node.outputs[i2.from_socket.name].float
                        pass            
            if out1.is_linked:
                 for o in out1.links:
                    if o.is_valid:
                        self.outputs["Set Vel"].float = (self.inputs["Channel 1"].float*(sfx.helpers[self.name].factor/100.0)+self.inputs["Channel 2"].float*(1.0-sfx.helpers[self.name].factor/100.0))
                        o.to_socket.node.inputs[o.to_socket.name].float = self.outputs["Set Vel"].float
                        sfx.helpers[self.name].Actuator_basic_props.diff_Vel                                     = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.diff_Vel
                        sfx.helpers[self.name].Actuator_basic_props.soll_Vel                                     = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.soll_Vel
                        sfx.helpers[self.name].Actuator_basic_props.ist_Pos                                      = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.ist_Pos
                        sfx.helpers[self.name].Actuator_basic_props.ist_Force                                    = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.ist_Force
                        sfx.helpers[self.name].Actuator_basic_props.ist_Vel                                      = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.ist_Vel
                        sfx.helpers[self.name].Actuator_basic_props.enable_Actuator                              = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.enable_Actuator
                        sfx.helpers[self.name].Actuator_basic_props.select_Actuator                              = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.select_Actuator
                        sfx.helpers[self.name].Actuator_basic_props.online_Actuator                              = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.online_Actuator
                        sfx.helpers[self.name].Actuator_basic_props.Status                                       = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Status
                        sfx.helpers[self.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop  = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
                        sfx.helpers[self.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop  = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
                        sfx.helpers[self.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop   = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop
                        sfx.helpers[self.name].Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop   = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop
                        sfx.helpers[self.name].Actuator_basic_props.Actuator_props.simple_actuator_confirm       = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_confirm
                        sfx.helpers[self.name].Actuator_basic_props.Actuator_props.simple_actuator_confirmed     = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.Actuator_props.simple_actuator_confirmed
                        sfx.helpers[self.name].Actuator_basic_props.DigTwin_basic_props.start_Loc                = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.DigTwin_basic_props.start_Loc
                        sfx.helpers[self.name].Actuator_basic_props.DigTwin_basic_props.con_Loc                  = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.DigTwin_basic_props.con_Loc
                        sfx.helpers[self.name].Actuator_basic_props.DigTwin_basic_props.end_Loc                  = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.DigTwin_basic_props.end_Loc
                        sfx.helpers[self.name].Actuator_basic_props.DigTwin_basic_props.length                   = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.DigTwin_basic_props.length
                        sfx.helpers[self.name].Actuator_basic_props.DigTwin_basic_props.mass_column1             = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.DigTwin_basic_props.mass_column1
                        sfx.helpers[self.name].Actuator_basic_props.DigTwin_basic_props.mass_column2             = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.DigTwin_basic_props.mass_column2
                        sfx.helpers[self.name].Actuator_basic_props.DigTwin_basic_props.mass_column3             = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.DigTwin_basic_props.mass_column3
                        sfx.helpers[self.name].Actuator_basic_props.DigTwin_basic_props.y_z_scale                = sfx.actuators[o.to_socket.node.name].Actuator_basic_props.DigTwin_basic_props.y_z_scale
 


