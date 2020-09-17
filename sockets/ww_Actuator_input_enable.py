import bpy

class ww_Actuator_input_enabel_socket(bpy.types.NodeSocket):
    '''ww Actuator Enabel'''
    bl_idname = 'ww_actuator_input_enable'
    bl_label = "ww Actuator Input Enable"

    enabel: bpy.props.BoolProperty(name = "enable",
                                        description = "enables the Actuator",
                                        default = False)

    def draw(self, context, layout, node, text):
            layout.prop(self, "enabel", text='enabel')

    # Socket color
    def draw_color(self, context, node):
        return (1.0,0,0, 0.5)