import bpy

class ww_input_Actuator_Socket(bpy.types.NodeSocket):
    '''ww Actuator Input Socket'''
    bl_idname = 'ww_input_Socket'
    bl_label = "ww Actuator Input Socket"

    set_Pos : bpy.props.FloatProperty(name = "Set Pos",
                                    description = "Set Position",
                                    precision = 3,
                                    default = 0.001)
    set_Vel : bpy.props.FloatProperty(name = "Set Vel",
                                    description = "Set Velocity",
                                    precision = 3,
                                    default = 0.001)
    set_Force : bpy.props.FloatProperty(name = "Set Force",
                                    description = "Set Force",
                                    precision = 3,
                                    default = 0.001)    

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
            layout.prop(self, "set_Pos")
            layout.prop(self, "set_Vel")
            layout.prop(self, "set_Force")

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)
