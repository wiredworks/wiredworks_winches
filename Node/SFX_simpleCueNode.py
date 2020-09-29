import bpy
from .. exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset

class SFX_simpleCueNode(bpy.types.Node):
    ''' Takes Joystick Data and outputs selected Data'''
    bl_idname = 'SFX_simpleCueNode'
    bl_label = 'simpleCue'
    bl_icon = 'ANCHOR_LEFT'
    bl_width_min = 220
    bl_width_max = 500

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    def update_value(self, context):
        self.update ()
        
    TickTime_prop : bpy.props.FloatProperty(default=0.0,
                                            update = update_value)

    demux_operator_started_bit1 : bpy.props.BoolProperty(name = "Demux Operator Started",
                                    description = "Demux Operator Started",
                                    default = False)
    demux_operator_running_modal: bpy.props.BoolProperty(name = "Demux Operator Running Modal",
                                    description = "Demux Operator Running Modal",
                                    default = False)

    def init(self, context):
        self.outputs.new('NodeSocketFloat', "Set Vel")
        self.outputs["Set Vel"].default_value = 0.0

        self.inputs.new('NodeSocketBool',name= 'Forward')
        self.inputs["Forward"].default_value = False

        self.inputs.new('NodeSocketBool',name= 'Reverse')
        self.inputs["Forward"].default_value = False

    def copy(self, node):
        print("copied node", node)
        
    def free(self):
        self.MotherNode.demux_operator_started_bit1 = False

    def draw_buttons(self, context, layout):
        box = layout.box()
        col = box.column()
        row4 = col.split(factor=0.75)         # Tick Time
        row5 = row4.split(factor=0.9)       # running modal
        row6 = row5.split(factor=0.9)       # started
        row7 = row6.split(factor=1)        # register
        row4.prop( self, 'TickTime_prop', text = '')
        row5.prop(self, 'demux_operator_running_modal', text = '')
        row6.prop(self, 'demux_operator_started_bit1', text = '')
        if not(self.demux_operator_started_bit1):
            row7.operator('sfx.simplecueop',text ='Start')
        else:
            row7.operator('sfx.commstarteddiag',text ='Started')

    def update(self):
        try:
            out1 = self.outputs["Set Vel"]
            inp1 = self.inputs["Forward"]
            inp2 = self.inputs["Reverse"]
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if inp1.is_linked:
                for i1 in inp1.links:
                    if i1.is_valid:
                        pass
            if inp2.is_linked:
                for i2 in inp1.links:
                    if i2.is_valid:
                        pass
            if out1.is_linked:
                 for o in out1.links:
                    if o.is_valid:
                        pass