import bpy

class SFX_OT_ww_RecoverDiag(bpy.types.Operator):
    ''' The Actuator is moved to the last synced Position before the E-Stop happened '''
    bl_idname = "sfx.ww_recoverdiag"
    bl_label = "Recover"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Moving to last Sync Position')
