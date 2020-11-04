import bpy

from .... exchange_data.sfx import sfx

class SFX_OT_simpleCue_IN(bpy.types.Operator):
    """ Insert an simple Cue Node to the Node Tree and start it"""
    bl_idname = "sfx.simplecue_in"
    bl_label = "Insert simple Cue Node"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        Node = bpy.data.node_groups[node_tree].nodes.new('SFX_simpleCue')
        bpy.data.node_groups[node_tree].nodes.active = Node
        sfx.cues[Node.name].operator_started = True
        bpy.ops.sfx.simplecue_op('INVOKE_DEFAULT')
        return {'FINISHED'}

    def draw(self,context):
        pass

