import bpy

class SFX_Act_out_ist_Pos(bpy.types.NodeSocket):
    '''SFX Actuator Output ist Pos'''
    bl_idname = 'SFX_act_out_ist_Pos'
    bl_label = "SFX Actuator Output Ist Pos"

    ist_pos: bpy.props.FloatProperty(name = "Ist Pos   ",
                                        description = "Ist Pos of Actuator",
                                        default = 0.0)

    def draw(self, context, layout, node, text):
            layout.prop(self, "ist_pos")

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)