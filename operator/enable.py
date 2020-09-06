import bpy

class EnableActuatorOperator(bpy.types.Operator):
    """ This operator connects the node to the Actuator"""
    bl_idname = "ww.actuator_enable"
    bl_label = "Actuator Enable"

    def execute(self, context):
        print(dir(context.active_node.Shared.ww_data))
        print('')
        print((context.active_node.Shared.ww_data))
        pass
        return {'FINISHED'}

    def invoke(self, context, event):
        pass
        return self.execute(context)