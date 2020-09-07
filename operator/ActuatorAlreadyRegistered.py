import bpy

class ActuatorAlreadyRegistred(bpy.types.Operator):
    ''' Actuator already registered '''
    bl_idname = "ww.actuator_already_registered"
    bl_label = "Actuator Already Registered"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Actuator already registered')
