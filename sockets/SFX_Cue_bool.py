import bpy

class SFX_Cue_bool(bpy.types.NodeSocket):
    '''SFX Bool Socket'''
    bl_idname = 'SFX_Cue_bool'
    bl_label = "SFX Bool Socket"

    default_value : bpy.props.BoolProperty(name = 'In',
                                           description = 'Bool Input',
                                           default = False)

    def draw(self, context, layout, node, text):
        layout.prop(self,'default_value',text=text)

    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)
    