import bpy

from .. exchange_data.ww_actuator_props import ww_Actuator_props
from .. exchange_data.ww_digtwin_basic_props import ww_DigTwin_basic_props 

class ww_Actuator_basic_props(bpy.types.PropertyGroup):
    bl_idname = "ww_Actuator_basic_props"

    ww_Actuator_props : bpy.props.PointerProperty(type = ww_Actuator_props)

    ww_DigTwin_basic_props : bpy.props.PointerProperty(type = ww_DigTwin_basic_props)


    # soll_Pos : bpy.props.FloatProperty(name = "Soll Pos",
    #                                 description = "Soll Position",
    #                                 precision = 3,
    #                                 default = 0.001)
    # ist_Pos : bpy.props.FloatProperty(name = "Ist Pos",
    #                                 description = "Ist Position",
    #                                 precision = 3,
    #                                 default = 0.001)
    # diff_Pos : bpy.props.FloatProperty(name = "Ist Pos",
    #                                 description = "Ist Position",
    #                                 precision = 3,
    #                                 default = 0.001)
    diff_Vel : bpy.props.FloatProperty(name = "Ist Pos",
                                    description = "Ist Position",
                                    precision = 3,
                                    default = 0.001)
    soll_Vel : bpy.props.FloatProperty(name = "Soll Vel",
                                    description = "Soll Velocity",
                                    precision = 3,
                                    default = 0.001)
    ist_Vel : bpy.props.FloatProperty(name = "Ist Vel",
                                    description = "Ist Velocity",
                                    precision = 3,
                                    default = 0.001)

    expand_DigTwin_basic : bpy.props.BoolProperty(name = "Expand Digital Twin Basic",
                                    description = " Expand Digital Twin Basic",
                                    default = False)
    expand_Actuator_setup : bpy.props.BoolProperty(name = "Expand Physical Actuator Setup",
                                    description = "Expand Physical Actuator Setup",
                                    default = False)

    def draw_ww_Actuator_basic_props(self, context, layout):
        box = layout.box()
        row = box.row()
        row.label(text='Basic Data')

        row = box.column(align = True)
        row1 = row.split(factor=0.15)
        col1 = row1.column()
        col1.label(text='Soll Vel')
        col1.prop(self,'soll_Vel', text = '')
        row2 = row1.split(factor=0.15)
        col2 = row2.column()
        col2.label(text='Ist Vel')
        col2.prop(self,'ist_Vel', text = '')
        row3 = row2.split(factor=0.2)
        col3 = row3.column()
        col3.label(text='Diff Vel')
        col3.prop(self,'diff_Vel', text = '')        
        row4 = row3.split(factor=0.35)
        col4 = row4.column()
        col4.label(text='')
        col4.operator('ww.actuator_main_reset',text ='Reset')
        row5 = row4.split(factor=0.45)
        col5 = row5.column()
        col5.label(text='')        
        col5.prop( self.ww_Actuator_props,'ww_actuator_State_prop', text = '')
        row6 = row5.split(factor=0.4)
        col6 = row6.column()
        col6.label(text='')            
        col6.prop( self.ww_Actuator_props,'ww_actuator_Temp_prop', text = '')
        row7 = row6.split(factor=0.8)
        col7 = row7.column()
        col7.label(text='')
        col7.prop( self.ww_Actuator_props,'ww_actuator_Amp_prop', text = '')            
        

        # split = box.split()
        # col = split.column()
        # col.label(text='Soll Pos')        
        # col.prop(self, 'soll_Pos' , text = '')
        # col = split.column()
        # col.label(text='Ist Pos')
        # col.prop(self, 'ist_Pos' , text = '')
        # col = split.column()
        # col.label(text='Diff Pos')
        # col.prop(self, 'diff_Pos' , text = '')
        # col = split.column()        
        # col.label(text='Diff Vel')
        # col.prop(self, 'diff_Vel' , text = '')
        # col = split.column()
        # col.label(text='Ist Vel')
        # col.prop(self, 'ist_Vel' , text = '')
        # col = split.column()
        # col.label(text='Soll Vel')
        # col.prop(self, 'soll_Vel' , text = '')

        row2 = box.row(align=True)
        row2.prop(self.ww_Actuator_props,"ww_actuator_Selected_prop",text="Selected")
        row2.prop(self.ww_Actuator_props,"ww_actuator_FBT_prop",text="FBT")
        row2.prop(self.ww_Actuator_props,"ww_actuator_Ready_prop",text="Ready")
        row2.prop(self.ww_Actuator_props,"ww_actuator_Online_prop",text="Online")
        row2.prop(self.ww_Actuator_props,"ww_actuator_Brake1_prop",text="Brake 1")
        row2.prop(self.ww_Actuator_props,"ww_actuator_Brake2_prop",text="Brake 2")
        row2.prop(self.ww_Actuator_props,"ww_actuator_Selected_prop",text="Selected")

        row3 = box.row(align=True)
        row3.prop(self, 'expand_DigTwin_basic')
        row3.prop(self, 'expand_Actuator_setup')


        if self.expand_DigTwin_basic:
            self.ww_DigTwin_basic_props.draw_ww_DigTwin_basic_props(context, layout) 

        if self.expand_Actuator_setup:
            self.ww_Actuator_props.drawActuatorSetup(context, layout) 