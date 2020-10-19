import bpy

class SFX_OT_MN_Stop(bpy.types.Operator):
    """ Stops the Operators asociated with the Nodes in the Node Tree"""
    bl_idname = "sfx.registermodals"
    bl_label = "Register OPS"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        for key in bpy.data.node_groups[node_tree].nodes.keys():
            Node = bpy.data.node_groups[node_tree].nodes[key]
            bpy.data.node_groups[node_tree].nodes.active = Node
            Node_root = Node.name.split('.')[0]
            if (Node_root == 'linrail' or
                Node_root == 'joystick'):
                Node.operator_restart = True
                Op = 'bpy.ops.sfx.'+Node_root+'_op(\'INVOKE_DEFAULT\')'
                exec(Op)
                Node.actuator_connected_bit1 = True
        return {'FINISHED'}

    def draw(self,context):
        pass

