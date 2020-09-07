import bpy

class EnableActuatorOperator(bpy.types.Operator):
    """ This operator is not yet implemented"""
    bl_idname = "ww.actuator_enable"
    bl_label = "Actuator Enable"

    def execute(self, context):
        pass
        return {'FINISHED'}

    def invoke(self, context, event):
        pass
        return self.execute(context)