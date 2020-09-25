import bpy

class SFX_OT_EnableDiag(bpy.types.Operator):
    """ This operator is not yet implemented"""
    bl_idname = "sfx.enablediag"
    bl_label = "Actuator Enable"

    def execute(self, context):
        pass
        return {'FINISHED'}

    def invoke(self, context, event):
        pass
        return self.execute(context)