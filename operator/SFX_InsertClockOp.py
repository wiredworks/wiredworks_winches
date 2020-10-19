import bpy

class SFX_OT_In_Clock(bpy.types.Operator):
    """ Insert a Clock Node to the Node Tree and start it"""
    bl_idname = "sfx.in_clock"
    bl_label = "Insert Clock Node"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        Node = bpy.data.node_groups[node_tree].nodes.new('SFX_ClockNode')
        bpy.data.node_groups[node_tree].nodes.active = Node
        bpy.ops.sfx.clockstartop('INVOKE_DEFAULT')
        return {'FINISHED'}

    def draw(self,context):
        pass

