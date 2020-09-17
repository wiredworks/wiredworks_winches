import bpy

from .. exchange_data.ww_Joystick_props import ww_Joystick_props 

class ww_Joystick_Socket(bpy.types.NodeSocket):
    '''ww Joystick Socket'''
    bl_idname = 'ww_Joystick_Socket'
    bl_label = "ww Joystick Socket"

    default_value : bpy.props.PointerProperty(type = ww_Joystick_props)

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)
