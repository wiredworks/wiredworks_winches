import bpy

class SFX_Socket_Float(bpy.types.NodeSocket):
    '''SFX Socket for Float'''
    bl_idname = 'SFX_Socket_Float'
    bl_label = "Float"

    float: bpy.props.FloatProperty(name = "Set Vel",
                                        description = "Set Vel for Actuator",
                                        default = 0.0)

    def draw(self, context, layout, node, text):
        row = layout.split(factor=0.2)
        row.prop(self, "float", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)