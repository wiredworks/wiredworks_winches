import bpy

class ww_Actuator_input_Set_Vel_socket(bpy.types.NodeSocket):
    '''ww Actuator Input set Vel'''
    bl_idname = 'ww_actuator_input_set_vel'
    bl_label = "ww Actuator Input Set Vel"

    set_vel: bpy.props.FloatProperty(name = "Set Vel",
                                        description = "Set Vel for Actuator",
                                        default = 0.0)

    def draw(self, context, layout, node, text):
        row = layout.split(factor=0.2)
        row.prop(self, "set_vel")

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)