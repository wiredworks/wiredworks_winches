import bpy

class ResetActuatorGuider(bpy.types.Operator):
    ''' Sends a reset Signal to the Guider Amplifiere '''
    bl_idname = "ww.actuator_guider_reset"
    bl_label = "Write"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Reset Guider Amplifier')
