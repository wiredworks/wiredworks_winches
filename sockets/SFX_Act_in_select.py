import bpy

class SFX_Act_in_select(bpy.types.NodeSocket):
    '''ww Actuator Enable'''
    bl_idname = 'SFX_Act_in_select'
    bl_label = "SFX Actuator Input Select"

    select: bpy.props.BoolProperty(name = "select",
                                        description = "selects the Actuator",
                                        default = False)

    def draw(self, context, layout, node, text):
            layout.prop(self, "select", text='select')

    # Socket color
    def draw_color(self, context, node):
        return (1.0,0,0, 0.5)