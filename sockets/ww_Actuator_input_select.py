import bpy

class ww_Actuator_input_select_socket(bpy.types.NodeSocket):
    '''ww Actuator Input select'''
    bl_idname = 'ww_actuator_input_select'
    bl_label = "ww Actuator Input Select"

    select: bpy.props.BoolProperty(name = "select",
                                        description = "selects the Actuator",
                                        default = False)

    def draw(self, context, layout, node, text):
            layout.prop(self, "select", text='select')

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)