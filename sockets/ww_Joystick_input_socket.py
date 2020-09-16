import bpy

class ww_Joystick_input_Socket(bpy.types.NodeSocket):
    '''ww Joystick Input Socket'''
    bl_idname = 'ww_Joystick_input_Socket'
    bl_label = "ww Joystick Input Socket"

    X_Achse : bpy.props.FloatProperty(name = "Joy X-Achse",
                                    description = "Joy X-Achse",
                                    precision = 3,
                                    default = 0.001)
    Y_Achse : bpy.props.FloatProperty(name = "Joy Y-Achse",
                                    description = "Joy Y-Achse",
                                    precision = 3,
                                    default = 0.001)
    Z_Achse : bpy.props.FloatProperty(name = "Joy Z-Achse",
                                    description = "Joy Z-Achse",
                                    precision = 3,
                                    default = 0.001)
    X_Rot : bpy.props.FloatProperty(name = "Joy X-Rot",
                                    description = "Joy X-Rot",
                                    precision = 3,
                                    default = 0.001)
    Y_Rot : bpy.props.FloatProperty(name = "Joy Y-Rot",
                                    description = "Joy Y-Rot",
                                    precision = 3,
                                    default = 0.001)
    Z_Rot : bpy.props.FloatProperty(name = "Joy Z-Rot",
                                    description = "Joy Z-Rot",
                                    precision = 3,
                                    default = 0.001)
    Button1 : bpy.props.BoolProperty(name = "Joy Button 1",
                                    description = "Joy Button 1",
                                    default = 0)
    Button2 : bpy.props.BoolProperty(name = "Joy Button 2",
                                    description = "Joy Button 2",
                                    default = 0)
    Button3 : bpy.props.BoolProperty(name = "Joy Button 3",
                                    description = "Joy Button 3",
                                    default = 0)
    Button4 : bpy.props.BoolProperty(name = "Joy Button 4",
                                    description = "Joy Button 4",
                                    default = 0)
    Button5 : bpy.props.BoolProperty(name = "Joy Button 5",
                                    description = "Button 5",
                                    default = 0)
    Button6 : bpy.props.BoolProperty(name = "Joy Button 6",
                                    description = "Button 6",
                                    default = 0)
    Button7 : bpy.props.BoolProperty(name = "Joy Button 7",
                                    description = "Button 7",
                                    default = 0)
    Button8 : bpy.props.BoolProperty(name = "Joy Button 8",
                                    description = "Button 8",
                                    default = 0)
    Button9 : bpy.props.BoolProperty(name = "Joy Button 9",
                                    description = "Button 9",
                                    default = 0)
    Button10: bpy.props.BoolProperty(name = "Joy Button 10",
                                    description = "Button 10",
                                    default = 0)
    Button11: bpy.props.BoolProperty(name = "Joy Button 11",
                                    description = "Button 11",
                                    default = 0)
    Button12: bpy.props.BoolProperty(name = "Joy Button 12",
                                    description = "Button 12",
                                    default = 0)                                                                                                                                                                                                                                                                                                                                                                                                            
    HAT_Switch : bpy.props.IntProperty(name = "Joy HAT-Switch",
                                    description = "Hat-Switch",
                                    default = 0)

    is_Pos : bpy.props.FloatProperty(name = "Is Pos",
                                    description = "IsSet Position",
                                    precision = 3,
                                    default = 0.001)
    is_Vel : bpy.props.FloatProperty(name = "Is Vel",
                                    description = "Is Velocity",
                                    precision = 3,
                                    default = 0.001)
    is_Force : bpy.props.FloatProperty(name = "Is Force",
                                    description = "Is Force",
                                    precision = 3,
                                    default = 0.001)    

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
            layout.label(text = "Joystick")


    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)
