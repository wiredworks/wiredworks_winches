import bpy

class ReSyncActuator(bpy.types.Operator):
    ''' The Actual Position is set as Synced '''
    bl_idname = "ww.actuator_resync"
    bl_label = "Write"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Setting Position as Synced')
