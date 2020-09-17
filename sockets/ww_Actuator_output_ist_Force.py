import bpy

class ww_Actuator_output_Ist_Force_socket(bpy.types.NodeSocket):
    '''ww Actuator Output ist Force'''
    bl_idname = 'ww_actuator_output_ist_force'
    bl_label = "ww Actuator Output Ist Force"

    ist_force: bpy.props.FloatProperty(name = "Ist Force",
                                        description = "Ist Force of Actuator",
                                        default = 0.0)

    def draw(self, context, layout, node, text):
            layout.prop(self, "ist_force")

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)