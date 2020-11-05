import bpy

from .. exchange_data.sfx import SFX_Joystick_Inset 

class SFX_Joy(bpy.types.NodeSocket):
    '''Joystick Socket'''
    bl_idname = 'SFX_Joy'
    bl_label = "ww Joystick Socket"

    default_value : bpy.props.PointerProperty(type = SFX_Joystick_Inset)

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)
