import bpy

class SFX_ww_DigTwin_Inset(bpy.types.PropertyGroup):
    ''' Dummy PlugIn Props'''
    bl_idname = "SFX_ww_DigTwin_Inset"

    ww_DigTwin_FloatA_prop : bpy.props.FloatProperty(name = "Float A",
                                    description = "A dummy Float",
                                    precision = 3,
                                    default = 0.001)
    ww_DigTwin_FloatB_prop : bpy.props.FloatProperty(name = "Float B",
                                    description = "A dummy Float",
                                    precision = 3,
                                    default = 0.001)

    def draw_ww_DigTwin_props(self, context, layout):
        box = layout.box()
        row = box.row()
        row.label(text='DigTwin Props')
        col = box.column(align = True)
        col.prop(self,'ww_DigTwin_FloatA_prop')
        col.prop(self,'ww_DigTwin_FloatB_prop')