import bpy

from .. exchange_data.ww_Joystick_props import ww_Joystick_props 

class ww_Joystick_input_Socket(bpy.types.NodeSocketStandard):
    '''ww Joystick Input Socket'''
    bl_idname = 'ww_Joystick_input_Socket'
    bl_label = "ww Joystick Input Socket"


    default_value = bpy.props.PointerProperty(type = ww_Joystick_props)
    
    # set_Pos : bpy.props.FloatProperty(name = "Set Pos",
    #                                 description = "Set Position",
    #                                 precision = 3,
    #                                 default = 0.001)
    # set_Vel : bpy.props.FloatProperty(name = "Set Vel",
    #                                 description = "Set Velocity",
    #                                 precision = 3,
    #                                 default = 0.001)
    # set_Force : bpy.props.FloatProperty(name = "Set Force",
    #                                 description = "Set Force",
    #                                 precision = 3,
    #                                 default = 0.001)    

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
            layout.label(text="Joystick")

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)
