import bpy

from .. exchange_data.ww_digtwin_props import ww_DigTwin_props

class ww_DigTwin_basic_props(bpy.types.PropertyGroup):
    bl_idname = "ww_DigTwin_basic_props"

    ww_DigTwin_props : bpy.props.PointerProperty(type = ww_DigTwin_props)

    def update_start_loc(self,context):
        bpy.context.collection.children[context.active_node.name].objects['Rail Actuator_In'].location=self.start_Loc
        pass

    def update_end_loc(self,context):
        bpy.context.collection.children[context.active_node.name].objects['Rail Actuator_Out'].location=self.end_Loc
        pass


    start_Loc : bpy.props.FloatVectorProperty(name = "Start Loc",
                                    description = "Start Location",
                                    precision = 3,
                                    default = (0.0,0.0,0.0),
                                    update = update_start_loc)
    end_Loc : bpy.props.FloatVectorProperty(name = "End Loc",
                                    description = "End Location",
                                    precision = 3,
                                    default = (0.0,0.0,0.0),
                                    update = update_end_loc)
    length : bpy.props.FloatProperty(name = "Length",
                                    description = "Length",
                                    precision = 3,
                                    default = 0.001)
    mass : bpy.props.FloatProperty(name = "Length",
                                    description = "Length",
                                    precision = 3,
                                    default = 0.001)

    expand_DigTwin_setup : bpy.props.BoolProperty(name = "Expand Digital Twin Setup",
                                    description = " Expand Digital Twin Setup",
                                    default = False)

    def draw_ww_DigTwin_basic_props(self, context, layout):
        box = layout.box()
        row = box.row()
        row.label(text='Digital Twin Basic Data')
        split = box.split()
        col = split.column()
        col.label(text='Start Loc')        
        col.prop(self, 'start_Loc' , text = '')
        col = split.column()
        col.label(text='End Loc')
        col.prop(self, 'end_Loc' , text = '')
        col = split.column()
        col.label(text='Lenght')
        col.prop(self, 'length' , text = '')
        col = split.column()        
        col.label(text='Mass')
        col.prop(self, 'mass' , text = '')

        row = box.row()
        row.prop(self,'expand_DigTwin_setup')            


        if self.expand_DigTwin_setup:
            self.ww_DigTwin_props.draw_ww_DigTwin_props(context, layout) 