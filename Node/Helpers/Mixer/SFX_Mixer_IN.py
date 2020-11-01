import bpy

from .... exchange_data.sfx import sfx

class SFX_OT_Mixer_IN(bpy.types.Operator):
    """ Insert a Mixer Node to the Node Tree and start it"""
    bl_idname = "sfx.mixer_in"
    bl_label = "Insert Mixer Node"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        Node = bpy.data.node_groups[node_tree].nodes.new('SFX_Mixer_Node')
        bpy.data.node_groups[node_tree].nodes.active = Node
        sfx.helpers[Node.name].operator_started = True
        bpy.ops.sfx.mixer_op('INVOKE_DEFAULT')
        return {'FINISHED'}

    def draw(self,context):
        pass

