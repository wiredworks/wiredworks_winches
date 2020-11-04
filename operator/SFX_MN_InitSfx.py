import bpy

from .. exchange_data.sfx import sfx

class SFX_OT_MN_InitSfx(bpy.types.Operator):
    """ Runs init_sfxData on all Nodes"""
    bl_idname = "sfx.initsfx"
    bl_label = "Init sfx"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        for key in bpy.data.node_groups[node_tree].nodes.keys():
            Node = bpy.data.node_groups[node_tree].nodes[key]
            bpy.data.node_groups[node_tree].nodes.active = Node
            bpy.data.node_groups[node_tree].nodes[Node.name].init_sfxData()
        return {'FINISHED'}

    def draw(self,context):
        pass

