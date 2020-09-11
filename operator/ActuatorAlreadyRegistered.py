import bpy

class ActuatorAlreadyRegistered(bpy.types.Operator):
    ''' Enabeles the editing of the Actuator properties '''
    bl_idname = "ww.actuator_already_registered"
    bl_label = "Edit"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Edit Actuator Properties')
