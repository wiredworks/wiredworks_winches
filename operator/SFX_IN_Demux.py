import bpy

class SFX_OT_IN_JoyDemux(bpy.types.Operator):
    """ Insert a JoyDemux Node to the Node Tree and start it"""
    bl_idname = "sfx.in_joydemux"
    bl_label = "Insert Demux Node"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        Node = bpy.data.node_groups[node_tree].nodes.new('SFX_JoyDemux_Node')
        bpy.data.node_groups[node_tree].nodes.active = Node
        bpy.ops.sfx.joydemux_op('INVOKE_DEFAULT')
        return {'FINISHED'}

    def draw(self,context):
        pass

