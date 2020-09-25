import bpy

class SFX_OT_ww_EngageDiag(bpy.types.Operator):
    ''' Canceles the edit of the Actuator properties '''
    bl_idname = "sfx.ww_engagediag"
    bl_label = "Engage"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Engage Guider')
