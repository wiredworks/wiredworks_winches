import bpy

class SFX_Socket_Bool(bpy.types.NodeSocket):
    '''SFX Socket for Bool'''
    bl_idname = 'SFX_Socket_Bool'
    bl_label = "Bool"

    bool: bpy.props.BoolProperty(name = "bool",
                                        description = "A Bool Socket",
                                        default = False)

    def draw(self, context, layout, node, text):
        layout.prop(self, "bool", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0,0,0, 0.5)