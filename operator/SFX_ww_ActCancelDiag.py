import bpy

class SFX_OT_ww_ActCancelDiag(bpy.types.Operator):
    ''' Canceles the edit of the Actuator properties '''
    bl_idname = "sfx.ww_actcanceldiag"
    bl_label = "Write"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Cancel Actuator Properties')
