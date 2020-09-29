import bpy

class SFX_Act_out_ist_Force(bpy.types.NodeSocket):
    '''SFX Actuator Output ist Force'''
    bl_idname = 'SFX_act_out_ist_Force'
    bl_label = "SFX Actuator Output Ist Force"

    ist_force: bpy.props.FloatProperty(name = "Ist Force",
                                        description = "Ist Force of Actuator",
                                        default = 0.0)

    def draw(self, context, layout, node, text):
            layout.prop(self, "ist_force")

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)