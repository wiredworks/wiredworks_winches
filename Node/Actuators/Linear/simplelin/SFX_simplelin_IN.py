import bpy

from ..... exchange_data.sfx import sfx

class SFX_OT_SimpleLin_IN(bpy.types.Operator):
    """ Insert a SimpleLin Node to the Node Tree and opens it"""
    bl_idname = "sfx.simplelin_in"
    bl_label = "Insert LinRail Node"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        Node = bpy.data.node_groups[node_tree].nodes.new('SFX_SimpleLin_Node')
        bpy.data.node_groups[node_tree].nodes.active = Node
        sfx.actuators[Node.name].operator_started = True
        bpy.ops.sfx.simplelin_op('INVOKE_DEFAULT')
        return {'FINISHED'}

    def draw(self,context):
        pass

