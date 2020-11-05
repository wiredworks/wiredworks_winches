import bpy

from .... exchange_data.sfx import sfx

class SFX_OT_JoyStick_IN(bpy.types.Operator):
    """ Insert a Joystick Node to the Node Tree and opens it"""
    bl_idname = "sfx.joystick_in"
    bl_label = "Insert Joystick Node"

    def invoke(self, context, event):
        node_tree = bpy.context.space_data.edit_tree.name
        Node = bpy.data.node_groups[node_tree].nodes.new('SFX_Joystick_Node')
        bpy.data.node_groups[node_tree].nodes.active = Node
        sfx.sensors[Node.name].operator_started = True
        bpy.ops.sfx.joystick_op('INVOKE_DEFAULT')
        return {'FINISHED'}

    def draw(self,context):
        pass

