import bpy

class SFX_OT_ActRegDiag(bpy.types.Operator):
    ''' Actuator Already registered '''
    bl_idname = "sfx.actregdiag"
    bl_label = "Registred"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Actuator Already Registred')
