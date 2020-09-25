import bpy

class SFX_OT_ww_ResetGuideDiag(bpy.types.Operator):
    ''' Sends a reset Signal to the Guider Amplifier '''
    bl_idname = "sfx.ww_resetguidediag"
    bl_label = "Reset"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Reset Guider Amplifier')
