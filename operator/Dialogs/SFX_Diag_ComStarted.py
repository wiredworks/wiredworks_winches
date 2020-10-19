import bpy

class SFX_OT_CommStartedDiag(bpy.types.Operator):
    bl_idname = "sfx.commstarteddiag"
    bl_label = "Comm Started"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Communication already started')
