import bpy

class ww_Actuator_output_Ist_Pos_socket(bpy.types.NodeSocket):
    '''ww Actuator Output ist Pos'''
    bl_idname = 'ww_actuator_output_ist_pos'
    bl_label = "ww Actuator Output Ist Pos"

    ist_pos: bpy.props.FloatProperty(name = "Ist Pos   ",
                                        description = "Ist Pos of Actuator",
                                        default = 0.0)

    def draw(self, context, layout, node, text):
            layout.prop(self, "ist_pos")

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)