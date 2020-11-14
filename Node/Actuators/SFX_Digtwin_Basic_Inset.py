import bpy

from . SFX_Digtwin_Expanded_Inset import SFX_Digtwin_Expanded_Inset

class SFX_Digtwin_Basic_Inset(bpy.types.PropertyGroup):
    '''Basic Properties for the Digital Twin'''
    bl_idname = "SXF_DigTwin_basic_Inset"

    DigTwin_props       : bpy.props.PointerProperty(type = SFX_Digtwin_Expanded_Inset)

    Mother_name         : bpy.props.StringProperty(name = "Mother Nodes Name",
                                        description = "Name of Mother Node",
                                        default = "")
    Mother_sfx_type     : bpy.props.StringProperty(name = "Mother sfx type",
                                        description = "Mother sfx type",
                                        default = "")

    Mother_sfx_sub_type : bpy.props.StringProperty(name = "Mother sfx sub type",
                                        description = "Mother sfx sub type",
                                        default = "")

    Mother_sfx_id       : bpy.props.StringProperty(name = "Mother sfx id",
                                        description = "Mother sfx id",
                                        default = "")

    def update_start_loc(self,context):
        if self.Mother_name != "" and self.Mother_sfx_sub_type == 'Linear':
            if self.Mother_sfx_id == 'linrail': 
                bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
                    objects[self.Mother_name+'_In'].location=self.start_Loc
            else:
                pass
        self.update_length(context)
        pass

    def update_end_loc(self,context):
        if self.Mother_name != "" and self.Mother_sfx_sub_type == 'Linear':
            if self.Mother_sfx_id == 'linrail':
                bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
                    objects[self.Mother_name+'_Out'].location=self.end_Loc
            else:
                pass
        self.update_length(context)
        pass

    def update_start_rot(self,context):
        self.update_length(context)
        pass

    def update_end_rot(self,context):
        self.update_length(context)
        pass

    def update_L(self,context):
        if self.Mother_name != "":
            self.update_length(context)
        pass

    def update_y_z_scale(self,context):
        if self.Mother_name != "":
            self.update_y_z_Scale(context)
        pass        

    start_Loc : bpy.props.FloatVectorProperty(name = "Start Loc",
                                    description = "Start Location",
                                    precision = 3,
                                    default = (0.0,0.0,0.0),
                                    update = update_start_loc)
    con_Loc : bpy.props.FloatVectorProperty(name = "Connector Loc",
                                    description = "Pos In Global",
                                    precision = 3,
                                    default = (0.0,0.0,0.0))
    end_Loc : bpy.props.FloatVectorProperty(name = "End Loc",
                                    description = "End Location",
                                    precision = 3,
                                    default = (0.0,0.0,0.0),
                                    update = update_end_loc)
    start_Rot : bpy.props.FloatProperty(name = "Start Rot",
                                    description = 'Start Rotation',
                                    precision = 3,
                                    default = -360,
                                    update = update_start_rot)
    con_Rot : bpy.props.FloatProperty(name = "Start Rot",
                                    description = 'Start Rotation',
                                    precision = 3,
                                    default = 0)
    end_Rot : bpy.props.FloatProperty(name = "Start Rot",
                                    description = 'Start Rotation',
                                    precision = 3,
                                    default = 360,
                                    update = update_end_rot)
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
                                    default = 1.0,
                                    update = update_y_z_scale)                                    

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
        if self.Mother_sfx_sub_type == 'Rotational' or self.Mother_sfx_id != 'linrail':
            col1.enabled = False
        else:
            col1.enabled = True       
        col1.label(text='Start Loc')        
        col1.prop(self, 'start_Loc' , text = '')
        split = row.split(factor = 1)
        col2 = split.column()
        col2.enabled = False
        col2.label(text='POS')
        col2.prop(self, 'con_Loc' , text = '')
        split = row.split(factor = 1)
        col3 = split.column()
        if self.Mother_sfx_sub_type == 'Rotational' or self.Mother_sfx_id != 'linrail':
            col3.enabled = False
        else:
            col3.enabled = True  
        col3.label(text='End Loc')
        col3.prop(self, 'end_Loc' , text = '')

        split = row.split(factor = 1)
        col4 = split.column()
 
        col4.label(text='Lenght')
        col4.prop(self, 'length' , text = '')
        col4.label(text ='Y-Z Scale')
        col4.prop(self, 'y_z_scale',text ='')
        split = row.split(factor = 1)
        col5 = split.column()        
        col5.label(text='Moment of Inertia')
        split = col5.split()
        col41 =split.column()
        col41.prop(self, 'mass_column1' , text = '')
        col42 =split.column()
        col42.prop(self, 'mass_column2' , text = '')
        col43 =split.column()
        col43.prop(self, 'mass_column3' , text = '')

        row = box.row()
        col6 = row.column(align = True)
        col7 = col6.split( factor = 0.43)
        col8 = col7.split( factor = 0.68)
        col9 = col8.split( factor = 0.5)
        col10 = col9.split( factor = 1)
        if self.Mother_sfx_sub_type == 'Linear':
            col8.enabled = False
            col9.enabled = False
            col10.enabled = False
        else:
            col8.enabled = True
            col9.enabled = True
            col10.enabled = True  
        col10.prop(self, 'start_Rot' , text = '')
        col9.prop(self, 'con_Rot' , text = '')
        col8.prop(self, 'end_Rot' , text = '')

        row = box.row()
        row.prop(self,'expand_DigTwin_setup')            


        if self.expand_DigTwin_setup:
            self.DigTwin_props.draw_ww_DigTwin_props(context, box)

    def update_length(self,context):
        if self.Mother_sfx_sub_type == 'Linear':
            if self.Mother_sfx_id == 'linrail':
                in_loc = bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
                    objects[self.Mother_name+'_In'].location
                out_loc = bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
                    objects[self.Mother_name+'_Out'].location
                normalized = (out_loc-in_loc).normalized()
                bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
                    objects[self.Mother_name+'_Out'].location = in_loc+self.length*normalized
                self.con_Loc =bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
                    objects[self.Mother_name+'_Connector'].matrix_world.to_translation()
            else:
                bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
                objects[self.Mother_name+'_Out'].location.x = self.length
                bpy.data.meshes[self.Mother_name].vertices[0].co.x = self.length
                bpy.data.meshes[self.Mother_name].vertices[7].co.x = self.length
                bpy.data.meshes[self.Mother_name].vertices[4].co.x = self.length
                bpy.data.meshes[self.Mother_name].vertices[3].co.x = self.length
                pass
        elif self.Mother_sfx_sub_type == 'Rotational':
            bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
            objects[self.Mother_name+'_Out'].location.x = self.length
            bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
            objects[self.Mother_name+'_Connector'].location.x = self.length
            for i in range(32,64):
                bpy.data.meshes[self.Mother_name].vertices[i].co.x = self.length
            pass
            bpy.data.meshes[self.Mother_name].vertices[65].co.x = self.length
        pass

    def update_y_z_Scale(self,context):
        print('Scale')
        bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
            objects[self.Mother_name].scale.y  = self.y_z_scale
        bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
            objects[self.Mother_name+'_In'].scale.y  = self.y_z_scale
        bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
            objects[self.Mother_name+'_Out'].scale.y  = self.y_z_scale
        bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
            objects[self.Mother_name].scale.z  = self.y_z_scale
        bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
            objects[self.Mother_name+'_In'].scale.z  = self.y_z_scale
        bpy.data.collections.get("ww SFX_Nodes").children[self.Mother_name].\
            objects[self.Mother_name+'_Out'].scale.z  = self.y_z_scale