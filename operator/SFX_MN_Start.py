import bpy

class SFX_OT_MN_Start(bpy.types.Operator):
    """ Starts the Operators asociated with the Nodes in the Node Tree"""
    bl_idname = "sfx.startmodals"
    bl_label = "Start OPS"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        for key in bpy.data.node_groups[node_tree].nodes.keys():
            Node = bpy.data.node_groups[node_tree].nodes[key]
            bpy.data.node_groups[node_tree].nodes.active = Node
            Node_root = Node.name.split('.')[0]
            if not(Node_root == 'linrail' or
                   Node_root == 'joystick'):
                Op = 'bpy.ops.sfx.'+Node_root+'_op(\'INVOKE_DEFAULT\')'
                exec(Op)
        return {'FINISHED'}

    def draw(self,context):
        pass

