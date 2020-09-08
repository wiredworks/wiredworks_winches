import bpy

class WriteActuatorProperties(bpy.types.Operator):
    ''' Writes the Actuator properties to the PLC '''
    bl_idname = "ww.actuator_props_write"
    bl_label = "Write"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self,context):
        self.layout.label(text='Write Actuator Properties')
