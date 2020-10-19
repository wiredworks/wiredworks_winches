import bpy

class SFX_OT_MN_Stop(bpy.types.Operator):
    """ Stops the Operators asociated with the Nodes in the Node Tree"""
    bl_idname = "sfx.stopmodals"
    bl_label = "Stop OPS"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        for key in bpy.data.node_groups[node_tree].nodes.keys():
            Node = bpy.data.node_groups[node_tree].nodes[key]
            bpy.data.node_groups[node_tree].nodes.active = Node
            Node_root = Node.name.split('.')
            print(Node_root)
            Node.operator_started = False
            Node.operator_running_modal = False
        return {'FINISHED'}

    def draw(self,context):
        pass

