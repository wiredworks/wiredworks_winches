import bpy

class ww_output_Actuator_Socket(bpy.types.NodeSocket):
    '''ww Actuator Output Socket'''
    bl_idname = 'ww_output_Socket'
    bl_label = "ww Actuator Output Socket"

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
            layout.prop(self, "is_Pos")
            layout.prop(self, "is_Vel")
            layout.prop(self, "is_Force")

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)
