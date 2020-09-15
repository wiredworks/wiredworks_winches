import bpy

class ww_output_Actuator_Socket(bpy.types.NodeSocket):
    '''ww Joystick Output Socket'''
    bl_idname = 'ww_Joystick_output_Socket'
    bl_label = "ww Joystick Output Socket"

    X_Achse : bpy.props.FloatProperty(name = "X-Achse",
                                    description = "X-Achse",
                                    precision = 3,
                                    default = 0.001)
    Y_Achse : bpy.props.FloatProperty(name = "Y-Achse",
                                    description = "Y-Achse",
                                    precision = 3,
                                    default = 0.001)
    Z_Achse : bpy.props.FloatProperty(name = "Z-Achse",
                                    description = "Z-Achse",
                                    precision = 3,
                                    default = 0.001)
    X_Rot : bpy.props.FloatProperty(name = "X-Rot",
                                    description = "X-Rot",
                                    precision = 3,
                                    default = 0.001)
    Y_Rot : bpy.props.FloatProperty(name = "Y-Rot",
                                    description = "Y-Rot",
                                    precision = 3,
                                    default = 0.001)
    Z_Rot : bpy.props.FloatProperty(name = "Z-Rot",
                                    description = "Z-Rot",
                                    precision = 3,
                                    default = 0.001)
    Button1 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button2 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button3 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button4 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button5 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button6 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button7 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button8 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button9 : bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button10: bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button11: bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)
    Button12: bpy.props.BoolProperty(name = "Button 1",
                                    description = "Button 1",
                                    default = 0)                                                                                                                                                                                                                                                                                                                                                                                                            
    HAT_Switch : bpy.props.IntProperty(name = "HAT-Switch",
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
            layout.prop(self, "X_Achse")
            layout.prop(self, "Y_Achse")
            layout.prop(self, "Z_Achse")

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)
