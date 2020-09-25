import bpy

class SFX_Act_in_enable(bpy.types.NodeSocket):
    '''ww Actuator Enable'''
    bl_idname = 'SFX_Act_in_enable'
    bl_label = "SFX Actuator Input Select"

    enable: bpy.props.BoolProperty(name = "enable",
                                        description = "enabeles the Actuator",
                                        default = False)

    def draw(self, context, layout, node, text):
            layout.prop(self, "enable", text='enable')

    # Socket color
    def draw_color(self, context, node):
        return (1.0,0,0, 0.5)