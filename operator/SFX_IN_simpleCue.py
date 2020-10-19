import bpy

class SFX_OT_IN_simpleCue(bpy.types.Operator):
    """ Insert an simple Cue Node to the Node Tree and start it"""
    bl_idname = "sfx.in_simplecue"
    bl_label = "Insert simple Cue Node"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        Node = bpy.data.node_groups[node_tree].nodes.new('SFX_simpleCue_Node')
        bpy.data.node_groups[node_tree].nodes.active = Node
        bpy.ops.sfx.simplecue_op('INVOKE_DEFAULT')
        return {'FINISHED'}

    def draw(self,context):
        pass

