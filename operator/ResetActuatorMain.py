import bpy

class ResetActuatorMain(bpy.types.Operator):
    ''' Sends a reset Signal to the Main Amplifier '''
    bl_idname = "ww.actuator_main_reset"
    bl_label = "Reset"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Reset Main Amplifier')
