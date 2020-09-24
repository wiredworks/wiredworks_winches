import bpy

from .. exchange_data.ww_Joystick_props import ww_Joystick_props 

class ww_Joystick_Float_Socket(bpy.types.NodeSocket):
    '''ww Joystick Socket'''
    bl_idname = 'ww_Joystick_float_Socket'
    bl_label = "ww Joystick Float Socket"

    default_value : bpy.props.PointerProperty(type = ww_Joystick_props)

    ww_Joy_items = (('Ptime','Ptime','Python Time'),
             ('Btime','Btime','Blender Time'),
             ('X_Achse','X-Achse','X-Achse Joystick'), 
             ('Y_Achse','Y-Achse','X_Achse Joystick'), 
             ('Z_Achse','Z-Achse','X_Achse Joystick'), 
             ('X_Rot','X-Rot','X_Rot Joystick'), 
             ('Y_Rot','Y-Rot','X_Rot Joystick'), 
             ('Z_Rot','Z-Rot','X_Rot Joystick'),
             ('Slider','Slider','Slider Joystick'))
             
    ww_enum_prop : bpy.props.EnumProperty(name='Joy Stick',
                                        description = 'Joystick Input',
                                        items = ww_Joy_items,
                                        default = 'X_Achse')

    ww_out_value : bpy.props.FloatProperty(name='Out',
                                            description = 'Output',
                                            default = 0)

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.prop(self,'ww_out_value')
        else:
            layout.prop(self, "ww_enum_prop", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)