import bpy

class SFX_Digtwin_Expanded_Inset(bpy.types.PropertyGroup):
    '''DigTwin Expanded Data'''
    bl_idname = "SFX_ww_DigTwin_Inset"

    FloatA : bpy.props.FloatProperty(name = "Float A",
                                    description = "A dummy Float",
                                    precision = 3,
                                    default = 0.001)
    FloatB : bpy.props.FloatProperty(name = "Float B",
                                    description = "A dummy Float",
                                    precision = 3,
                                    default = 0.001)

    def draw_ww_DigTwin_props(self, context, layout):
        box = layout.box()
        row = box.row()
        row.label(text='DigTwin Expanded Data')
        col = box.column(align = True)
        col.prop(self,'FloatA')
        col.prop(self,'FloatB')