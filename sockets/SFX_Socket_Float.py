import bpy

class SFX_Socket_Float(bpy.types.NodeSocket):
    '''SFX Socket for Float'''
    bl_idname = 'SFX_Socket_Float'
    bl_label = "Float"

    float: bpy.props.FloatProperty(name = "Float",
                                        description = "Float",
                                        default = 0.0)

    def draw(self, context, layout, node, text):

        if self.is_output:
            col = layout.column(align = True)
            col1 = col.split(factor = 0.85)
            col2 = col1.split(factor = 0.85)
            col3 = col2.split(factor = 1)
            col1.prop(self, "float", text='')
            col2.label(text = text)
        else:
            col = layout.column(align = True)
            col1 = col.split(factor = 0.30)
            col2 = col1.split(factor = 0.5)
            col3 = col2.split(factor = 1)               
            col1.label(text = '')
            col3.prop(self, "float", text='')
            col2.label(text = text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)