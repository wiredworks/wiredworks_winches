import bpy

class ww_Actuator_output_Ist_Vel_socket(bpy.types.NodeSocket):
    '''ww Actuator Output ist Vel'''
    bl_idname = 'ww_actuator_output_ist_vel'
    bl_label = "ww Actuator Output Ist Vel"

    ist_vel: bpy.props.FloatProperty(name = "Ist Vel   ",
                                        description = "Ist Vel of Actuator",
                                        default = 0.0)

    def draw(self, context, layout, node, text):
            layout.prop(self, "ist_vel")

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)