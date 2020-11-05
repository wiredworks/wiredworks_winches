import bpy

from .. exchange_data.sfx import SFX_Joystick_Inset 

class SFX_Joy_bool(bpy.types.NodeSocket):
    '''ww Joystick Socket'''
    bl_idname = 'SFX_Joy_bool'
    bl_label = "ww Joystick Bool Socket"

    default_value : bpy.props.PointerProperty(type = SFX_Joystick_Inset)

    ww_Joy_items = (('Button1','Button 1','Button 1'),
                    ('Button2','Button 2','Button 2'),
                    ('Button3','Button 3','Button 3'), 
                    ('Button4','Button 4','Button 4'),
                    ('Button5','Button 5','Button 5'),
                    ('Button6','Button 6','Button 6'),
                    ('Button7','Button 7','Button 7'),
                    ('Button8','Button 8','Button 8'),
                    ('Button9','Button 9','Button 9'),
                    ('Button10','Button 10','Button 10'),
                    ('Button11','Button 11','Button 11'),
                    ('Button12','Button 12','Button 12'))

    ww_enum_prop : bpy.props.EnumProperty(name='Joy Stick',
                                        description = 'Joystick Input',
                                        items = ww_Joy_items,
                                        default = 'Button1')

    ww_out : bpy.props.BoolProperty(name='Out',
                                    description = 'Output',
                                    default = False)

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.prop(self,'ww_out')
        else:
            layout.prop(self, "ww_enum_prop", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)