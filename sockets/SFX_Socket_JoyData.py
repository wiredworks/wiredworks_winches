import bpy

from .. exchange_data.sfx import SFX_Joystick_Inset 

class SFX_Socket_JoyData(bpy.types.NodeSocket):
    '''Transports Joystick Data '''
    bl_idname = 'SFX_Socket_JoyData'
    bl_label = "Joystick Data"

    default_value : bpy.props.PointerProperty(type = SFX_Joystick_Inset)
            
    def draw(self, context, layout, node, text):
        layout.label(text=text)
        
    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)