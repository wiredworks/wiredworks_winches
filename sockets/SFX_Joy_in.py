import bpy

from .. exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset 

class SFX_Joy_in(bpy.types.NodeSocketStandard):
    '''SFX_Joystick_Inset '''
    bl_idname = 'SFX_Joy_in'
    bl_label = "ww Joystick Input Socket"

    default_value = bpy.props.PointerProperty(type = SFX_Joystick_Inset)
   

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
            layout.label(text="Joystick")

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)