import bpy

from .. exchange_data.sfx import SFX_Joystick_Inset 

class SFX_Cue_Float(bpy.types.NodeSocket):
    '''Joystick Socket'''
    bl_idname = 'SFX_Cue_Float'
    bl_label = "Cue Float Socket"

    default_value : bpy.props.PointerProperty(type = SFX_Joystick_Inset)

    ww_out_value : bpy.props.FloatProperty(name='Out',
                                            description = 'Output',
                                            default = 0)

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        layout.prop(self,'ww_out_value')

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)