import bpy

class ConnectorAlreadyStarted(bpy.types.Operator):
    bl_idname = "ww.connector_already_started"
    bl_label = "Connector Already Started"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Connector already started')
