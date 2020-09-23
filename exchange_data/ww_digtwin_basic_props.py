import bpy

from .. exchange_data.ww_digtwin_props import ww_DigTwin_props

class ww_DigTwin_basic_props(bpy.types.PropertyGroup):
    bl_idname = "ww_DigTwin_basic_props"

    ww_DigTwin_props : bpy.props.PointerProperty(type = ww_DigTwin_props)

    def update_start_loc(self,context):
        bpy.context.collection.children[context.active_node.name].objects[context.active_node.name+'_In'].location=self.start_Loc
        self.update_length(self,context)
        pass

    def update_end_loc(self,context):
        bpy.context.collection.children[context.active_node.name].objects[context.active_node.name+'_Out'].location=self.end_Loc
        self.update_length(self,context)
        pass

    def update_length(self,context):
        in_loc = bpy.context.collection.children[context.active_node.name].objects[context.active_node.name+'_In'].location
        out_loc = bpy.context.collection.children[context.active_node.name].objects[context.active_node.name+'_Out'].location
        normalized = (out_loc-in_loc).normalized()
        bpy.context.collection.children[context.active_node.name].objects[context.active_node.name+'_Out'].location =\
            in_loc+self.length*normalized
        pass


    start_Loc : bpy.props.FloatVectorProperty(name = "Start Loc",
                                    description = "Start Location",
                                    precision = 3,
                                    default = (0.0,0.0,0.0),
                                    update = update_start_loc)
    con_Loc : bpy.props.FloatVectorProperty(name = "Connector Loc",
                                    description = "Pos In Global",
                                    precision = 3,
                                    default = (0.0,0.0,0.0),
                                    update = update_end_loc)
    end_Loc : bpy.props.FloatVectorProperty(name = "End Loc",
                                    description = "End Location",
                                    precision = 3,
                                    default = (0.0,0.0,0.0),
                                    update = update_end_loc)
    length : bpy.props.FloatProperty(name = "Length",
                                    description = "Length",
                                    precision = 3,
                                    default = 0.001,
                                    update = update_length)
    mass_column1 : bpy.props.FloatVectorProperty(name = "Moment of Inertia",
                                    description = "Moment of Inertia First Column",
                                        precision = 3,
                                    default = (0.0,0.0,0.0))
    mass_column2 : bpy.props.FloatVectorProperty(name = "Moment of Inertia",
                                    description = "Moment of Inertia Second Column",
                                    precision = 3,
                                    default = (0.0,0.0,0.0))
    mass_column3 : bpy.props.FloatVectorProperty(name = "Moment of Inertia",
                                    description = "Moment of Inertia Third Column",
                                    precision = 3,
                                    default = (0.0,0.0,0.0))
    y_z_scale : bpy.props.FloatProperty(name = "Y-Z Scale",
                                    description = "Moment of Inertia Third Column",
                                    precision = 3,
                                    default = 1.0)                                    

    expand_DigTwin_setup : bpy.props.BoolProperty(name = "Expand Digital Twin Setup",
                                    description = " Expand Digital Twin Setup",
                                    default = False)


    def draw_ww_DigTwin_basic_props(self, context, layout):
        box = layout.box()
        row = box.row()
        row.label(text='Digital Twin Basic Data')
        row = box.row()        
        split = row.split(factor = 1)
        col1 = split.column()
        col1.label(text='Start Loc')        
        col1.prop(self, 'start_Loc' , text = '')
        split = row.split(factor = 1)
        col2 = split.column()
        col2.label(text='POS')
        col2.prop(self, 'con_Loc' , text = '')
        split = row.split(factor = 1)
        col2 = split.column()
        col2.label(text='End Loc')
        col2.prop(self, 'end_Loc' , text = '')
        split = row.split(factor = 1)
        col3 = split.column()
        col3.label(text='Lenght')
        col3.prop(self, 'length' , text = '')
        col3.label(text ='Y-Z Scale')
        col3.prop(self, 'y_z_scale',text ='')
        split = row.split(factor = 1)
        col4 = split.column()        
        col4.label(text='Moment of Inertia')
        split = col4.split()
        col41 =split.column()
        col41.prop(self, 'mass_column1' , text = '')
        col42 =split.column()
        col42.prop(self, 'mass_column2' , text = '')
        col43 =split.column()
        col43.prop(self, 'mass_column3' , text = '')

        row = box.row()
        row.prop(self,'expand_DigTwin_setup')            


        if self.expand_DigTwin_setup:
            self.ww_DigTwin_props.draw_ww_DigTwin_props(context, layout) 