import bpy

from .... exchange_data.sfx import sfx

class SFX_OT_LinRail_IN(bpy.types.Operator):
    """ Insert a LinRail Node to the Node Tree and opens it"""
    bl_idname = "sfx.simplerot_in"
    bl_label = "Insert SimpleRot Node"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        Node = bpy.data.node_groups[node_tree].nodes.new('SFX_SimpleRot_Node')
        bpy.data.node_groups[node_tree].nodes.active = Node
        sfx.actuators[Node.name].operator_started = True
        bpy.ops.sfx.simplerot_op('INVOKE_DEFAULT')
        return {'FINISHED'}

    def draw(self,context):
        pass

