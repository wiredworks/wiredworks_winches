import bpy

from .. exchange_data.SFX_ww_digtwin_Inset import SFX_ww_DigTwin_Inset

class SFX_DigTwin_basic_Inset(bpy.types.PropertyGroup):
    '''Basic Properties for the Digital Twin'''
    bl_idname = "SXF_DigTwin_basic_Inset"

    DigTwin_props : bpy.props.PointerProperty(type = SFX_ww_DigTwin_Inset)

    Mother_name   : bpy.props.StringProperty(name = "Mother Nodes Name",
                                        description = "Name of Mother Node",
                                        default = "")

    def update_start_loc(self,context):
        bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].objects[self.Mother_name+'_In'].location=self.start_Loc
        self.update_length(context)
        pass

    def update_end_loc(self,context):
        bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].objects[self.Mother_name+'_Out'].location=self.end_Loc
        self.update_length(context)
        pass

    def update_L(self,context):
        self.update_length(context)
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
                                    update = update_L)
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
            self.DigTwin_props.draw_DigTwin_props(context, layout)

    def update_length(self,context):
        in_loc = bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].objects[self.Mother_name+'_In'].location
        out_loc = bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].objects[self.Mother_name+'_Out'].location
        normalized = (out_loc-in_loc).normalized()
        bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].objects[self.Mother_name+'_Out'].location =\
            in_loc+self.length*normalized
        #context.active_node.Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop= self.length
        #super().super().Actuator_props.simple_actuator_HardMax_prop= self.length
        # super().__init__()
        # print(dir(super()))
        pass