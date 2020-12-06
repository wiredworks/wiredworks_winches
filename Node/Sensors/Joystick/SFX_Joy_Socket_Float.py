import bpy

from .... exchange_data.sfx import SFX_Joystick_Inset 

class SFX_Joy_Socket_Float(bpy.types.NodeSocket):
    '''Selects Joystick Axis Data'''
    bl_idname = 'SFX_Joy_Socket_Float'
    bl_label = "Joystick Float Socket"

    default_value : bpy.props.PointerProperty(type = SFX_Joystick_Inset)

    Joy_items = (('Ptime','Ptime','Python Time'),
             ('Btime','Btime','Blender Time'),
             ('X_Achse','X-Achse','X-Achse Joystick'), 
             ('Y_Achse','Y-Achse','X_Achse Joystick'), 
             ('Z_Achse','Z-Achse','X_Achse Joystick'), 
             ('X_Rot','X-Rot','X_Rot Joystick'), 
             ('Y_Rot','Y-Rot','X_Rot Joystick'), 
             ('Z_Rot','Z-Rot','X_Rot Joystick'),
             ('Slider','Slider','Slider Joystick'))
             
    enum_prop : bpy.props.EnumProperty(name='Joy Stick',
                                        description = 'Joystick Input',
                                        items = Joy_items,
                                        default = 'X_Achse')

    float : bpy.props.FloatProperty(name='Out',
                                            description = 'Output',
                                            default = 0)

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text= self.enum_prop)
            layout.prop(self,'float', text = '')
        else:
            layout.prop(self, "enum_prop", text='')

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)