import bpy

from .. exchange_data.sfx import sfx

class SFX_OT_MN_Stop(bpy.types.Operator):
    """ Stops the Operators asociated with the Nodes in the Node Tree"""
    bl_idname = "sfx.stopmodals"
    bl_label = "Stop OPS"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        for key in bpy.data.node_groups[node_tree].nodes.keys():
            Node = bpy.data.node_groups[node_tree].nodes[key]
            bpy.data.node_groups[node_tree].nodes.active = Node
            try:
                sfx.clocks[Node.name].operator_started           = False
                sfx.clocks[Node.name].operator_running_modal     = False
            except KeyError:
                pass
            try:
                sfx.helpers[Node.name].operator_started          = False
                sfx.helpers[Node.name].operator_running_modal    = False
            except KeyError:
                pass
            try:
                sfx.cues[Node.name].operator_started             = False
                sfx.cues[Node.name].operator_running_modal       = False
            except KeyError:
                pass
            try:
                sfx.kinematics[Node.name].operator_started       = False
                sfx.kinematics[Node.name].operator_running_modal = False
            except KeyError:
                pass
        return {'FINISHED'}

    def draw(self,context):
        pass

