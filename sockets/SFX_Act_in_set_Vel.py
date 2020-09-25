import bpy

class SFX_Act_in_set_Vel(bpy.types.NodeSocket):
    '''ww Actuator Input set Vel'''
    bl_idname = 'SFX_act_in_set_Vel'
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