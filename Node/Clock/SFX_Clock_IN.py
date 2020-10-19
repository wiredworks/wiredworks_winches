import bpy

class SFX_OT_Clock_IN(bpy.types.Operator):
    """ Insert a Clock Node to the Node Tree and start it"""
    bl_idname = "sfx.clock_in"
    bl_label = "Insert Clock Node"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        Node = bpy.data.node_groups[node_tree].nodes.new('SFX_Clock_Node')
        bpy.data.node_groups[node_tree].nodes.active = Node
        bpy.ops.sfx.clock_op('INVOKE_DEFAULT')
        return {'FINISHED'}

    def draw(self,context):
        pass

