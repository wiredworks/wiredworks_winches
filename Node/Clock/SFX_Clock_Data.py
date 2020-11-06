import bpy

from ... exchange_data.sfx import sfx

class clock(bpy.types.PropertyGroup):
    ''' Defines sfx_clock'''
    bl_idname = "sfx_clock"

    def a_update(self,context):
        self.sfx_update(context)

    operator_started : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
                                    default = False,
                                    update = a_update)
    operator_running_modal: bpy.props.BoolProperty(name = "Operator Running Modal",
                                    description = "Operator Running Modal",
                                    default = False)
    date :bpy.props.StringProperty(name='Date',
                                    description='Date',
                                    default = 'Sun Jun 20 23:21:05 1993')
    TickTime_prop: bpy.props.FloatProperty(name = "Tick Time",
                                    description ="Sanity Check message round trip Time",
                                    default=0.1,
                                    precision=2)

    def sfx_update(self,context):
        self.MotherNode = context.active_node
        if self.operator_started:
            Node_root = self.MotherNode.name.split('.')[0]
            Op = 'bpy.ops.sfx.'+Node_root+'_op(\'INVOKE_DEFAULT\')'
            exec(Op)
        else:
            sfx.clocks[self.MotherNode.name].operator_running_modal = False
            node_tree = bpy.context.space_data.edit_tree.name
            for key in bpy.data.node_groups[node_tree].nodes.keys():
                Node = bpy.data.node_groups[node_tree].nodes[key]
                bpy.data.node_groups[node_tree].nodes.active = Node
                try:
                    sfx.sensors[Node.name].operator_running_modal    = False
                except KeyError:
                    pass
                try:
                    sfx.cues[Node.name].operator_running_modal       = False
                except KeyError:
                    pass
                try:
                    sfx.kinematics[Node.name].operator_running_modal = False
                except KeyError:
                    pass
                try:
                    sfx.helpers[Node.name].operator_running_modal    = False
                except KeyError:
                    pass
                try:
                    sfx.actuators[Node.name].operator_running_modal    = False
                except KeyError:
                    pass
                Node.sfx_update() 