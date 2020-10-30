import bpy
import time

class SFX_OT_InsertClockOp(bpy.types.Operator):
    """ This operator ..."""
    bl_idname = "sfx.insertclockop"
    bl_label = "Insert Clock"

    def invoke(self, context, event):
        #print(dir(context))
        Node = bpy.data.node_groups['NodeTree'].nodes.new('SFX_ClockNode')
        bpy.data.node_groups['NodeTree'].nodes.active = Node
        bpy.ops.sfx.clockstartop('INVOKE_DEFAULT')


    def draw(self,context):
        pass

