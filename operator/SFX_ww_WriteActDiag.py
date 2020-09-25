import bpy

class SFX_OT_WriteActDiag(bpy.types.Operator):
    ''' Writes the Actuator properties to the PLC '''
    bl_idname = "sfx.ww_writeactdiag"
    bl_label = "Write"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Write Actuator Properties')
