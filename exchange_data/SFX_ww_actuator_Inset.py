import bpy

class SFX_ww_Actuator_props(bpy.types.PropertyGroup):
    ''' Actuator Plug In for the wiredworks winches'''
    bl_idname = "SFX_ww_Actuator_Inset"

    ww_State_items = [
        ("Disabeled","Disabeled","",1),
        ("En-abeled","En-abeled","",2),
        ("E-Stopped","E-Stopped","",3)
        ]
    def get_enum_State(self):
        import random
        return random.randint(1,3)
    def set_enum_State(self,value):
        print("setting State value ",value)


    ww_Guider_Clutch_items = [
        ("Engaged","Engaged","",1),
        ("Dis-Engaged","Dis-Engaged","",2)
        ]
    def get_enum_Guider_Clutch(self):
        import random
        return random.randint(1,2)
    def set_enum_Guider_Clutch(self,value):
        print("setting Guider Value ",value)

    ww_actuator_Selected_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_FBT_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_Ready_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_Online_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_Brake1_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_Brake2_prop: bpy.props.BoolProperty(default=True) 

    ww_actuator_Amp_prop: bpy.props.FloatProperty(name = "Ampere",
                                                                description ="Amplifier Output",
                                                                default=999,
                                                                precision=0) 
    ww_actuator_State_prop: bpy.props.EnumProperty(items=ww_State_items,
                                                   get=get_enum_State,
                                                   set=set_enum_State)
    ww_actuator_Temp_prop: bpy.props.FloatProperty(name = "Temperature",
                                                                description ="Amplifier Tempeprature",
                                                                default=99,
                                                                precision=0)
    ww_actuator_Positions_HardMax_prop: bpy.props.FloatProperty(name = "Hard Max",
                                                                description ="Maximum Position set in the PLC",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Positions_UserMax_prop: bpy.props.FloatProperty(name = "User Max",
                                                                description ="Maximum Position set in Program",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Positions_ActPos_prop: bpy.props.FloatProperty(name = "Act Pos",
                                                                description ="Actual Position",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Positions_UserMin_prop: bpy.props.FloatProperty(name = "User Min",
                                                                description ="Minimum Position set in Program",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Positions_HardMin_prop: bpy.props.FloatProperty(name = "Hard Min",
                                                                description ="Minimum Position set in the PLC",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Positions_PosWin_prop: bpy.props.FloatProperty(name = "Pos Win",
                                                                description ="Max Diff between IstPos and SetPos",
                                                                default=99.99,
                                                                precision=3)
    ww_actuator_VelAccAmp_VelMaxMot_prop: bpy.props.FloatProperty(name = "Vel Max Motor",
                                                                description ="Maximum Speed the Motor can run at",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_VelAccAmp_VelMax_prop: bpy.props.FloatProperty(name = "Vel Max",
                                                                description ="Maximum Velocity set in Program",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_VelAccAmp_AccMax_prop: bpy.props.FloatProperty(name = "Acc Max",
                                                                description ="Maximum Acceleration",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_VelAccAmp_DccMax_prop: bpy.props.FloatProperty(name = "Dcc Max",
                                                                description ="Maximum Deceleration",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_VelAccAmp_AccMove_prop: bpy.props.FloatProperty(name = "Acc Max Move",
                                                                description ="Maximum Acceleration while traveling along a Path",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_VelAccAmp_MaxAmp_prop: bpy.props.FloatProperty(name = "Amp Max",
                                                                description ="Maximal Ampere output of Amplifier in %",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_VelAccAmp_VelWin_prop: bpy.props.FloatProperty(name = "Vel Win",
                                                                description ="Max Diff between IstVel and SetVel",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Filter_LagErr_prop: bpy.props.FloatProperty(name = "Lag Err",
                                                                description ="Diff between IstPos and SetPos",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Filter_Prop_prop: bpy.props.FloatProperty(name = "P Filter",
                                                                description ="P Constant of PID-Filter",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Filter_Int_prop: bpy.props.FloatProperty(name = "I Filter",
                                                                description ="I Constant of PID-Filter",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Filter_Der_prop: bpy.props.FloatProperty(name = "D Filter",
                                                                description ="D Constant of PID-Filter",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Filter_IntLim_prop: bpy.props.FloatProperty(name = "I Limit",
                                                                description ="Limit for the buildup of the I faktor of PID-Filter",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Filter_Rampform_prop: bpy.props.FloatProperty(name = "Rampform",
                                                                description ="Sanity check",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Rope_SWLL_prop: bpy.props.FloatProperty(name = "SWLL Rope",
                                                                description ="Safe Working Load Limit of the Rope",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Rope_Diameter_prop: bpy.props.FloatProperty(name = "Rope Diameter",
                                                                description ="Rope Diameter",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Rope_Type_prop: bpy.props.FloatProperty(name = "Rope Type",
                                                                description ="Rope Type",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Rope_Number_prop: bpy.props.FloatProperty(name = "Rope Number",
                                                                description ="Rope Number",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Rope_Length_prop: bpy.props.FloatProperty(name = "Rope Length",
                                                                description ="Rope Length",
                                                                default=999.99,
                                                                precision=3)
    # Guider properties of 3D-Control
    ww_actuator_Guider_Pos_prop: bpy.props.FloatProperty(name = "Guider Position",
                                                                description ="Position of the Guider",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Guider_Clutch_prop: bpy.props.EnumProperty(items=ww_Guider_Clutch_items, get=get_enum_Guider_Clutch, set=set_enum_Guider_Clutch)
    ww_actuator_Guider_Vel_prop: bpy.props.FloatProperty(name = "Guider Velocity",
                                                                description ="Velocity of the Guider",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Guider_State_prop: bpy.props.EnumProperty(items=ww_State_items, get=get_enum_State, set=set_enum_State) 
    ww_actuator_Guider_Ready_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_Guider_Online_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_Guider_Pitch_prop: bpy.props.FloatProperty(name = "Guider Pitch",
                                                                description ="Distance the Guider travels for one Rotation of Main Drum",
                                                                default=6.3,
                                                                precision=2)
    ww_actuator_Guider_PosMax_prop: bpy.props.FloatProperty(name ="Guider Max Pos",
                                                                description ="Maximum Position of the the Guider",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Guider_PosMin_prop: bpy.props.FloatProperty(name ="Guider Min Pos",
                                                                description ="Minimum Position of the the Guider",
                                                                default=999.99,
                                                                precision=3)
    # Recover
    ww_actuator_Recover_CutPos_prop: bpy.props.FloatProperty(name ="Recover Cut Position",
                                                                description ="Position at E-Stop",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Recover_CutVel_prop: bpy.props.FloatProperty(name ="Recover Cut Velocity",
                                                                description ="Velocity",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Recover_CutTime_prop: bpy.props.FloatProperty(name ="Time of E-Stop",
                                                                description ="Time of E-Stop",
                                                                default=999.99,
                                                                precision=3)
    ww_actuator_Recover_PosDiff_prop: bpy.props.FloatProperty(name ="Diff Pos at E-Stop",
                                                                description ="Diff between SetPos and ActPos after coming to Halt",
                                                                default=999.99,
                                                                precision=3)
    # E-Stop Handling
    ww_actuator_EStop_Master_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_Slave_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_Network_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_EStop1_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_EStop2_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_30kW_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_05kW_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_Brk1_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_Brk2_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_Brk2Kb_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_SPS_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_Red_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_Enc_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_PosWin_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_VelWin_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_Endlage_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_G1Com_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_G1Out_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_G1FB_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_G2Com_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_G2Out_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_G2FB_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_G3Com_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_G3Out_prop: bpy.props.BoolProperty(default=True)
    ww_actuator_EStop_G3FB_prop: bpy.props.BoolProperty(default=True)

    def drawActuatorSetup(self, context, layout):

        boxA = layout.box()
        row = boxA.row()
        row.label(text='Physical Actuator Setup')        
        box1 = boxA.split()
        
        splitA = box1.split()

        colA = splitA.column(align=True)
        box = colA.box()
        row = box.row(align=True)
        row.label(text="Positions")
        row = box.row(align=True)
        row.operator('ww.actuator_props_edit',text ='Edit')
        split = box.split()
        col1 = split.column()
        col1.label(text="Hard Max:") 
        col1.label(text="User Max:")
        col1.label(text="Act Pos:")
        col1.label(text="User Min:")
        col1.label(text="Hard Min:")
        col1.label(text="Pos Win:")
        col1.label(text="")
        col1.operator('ww.actuator_props_write',text ='Write')
        col2 = split.column()      
        col2.prop(self,"ww_actuator_Positions_HardMax_prop",text="")
        col2.prop(self,"ww_actuator_Positions_UserMax_prop",text="")
        col2.prop(self,"ww_actuator_Positions_ActPos_prop",text="")
        col2.prop(self,"ww_actuator_Positions_UserMin_prop",text="")
        col2.prop(self,"ww_actuator_Positions_HardMin_prop",text="")
        col2.prop(self,"ww_actuator_Positions_PosWin_prop",text="")
        col2.label(text="")
        col2.operator('ww.actuator_props_cancel',text ='Cancel')

        colB = splitA.column(align=True)        
        box = colB.box() 
        row = box.row(align=True)
        row.label(text="Vel/Acc/Amp")
        row = box.row(align=True)
        row.operator('ww.actuator_props_edit',text ='Edit')
        split = box.split()
        col = split.column()
        col.label(text="VelMaxMot:")
        col.label(text="VelMax:") 
        col.label(text="AccMax:")
        col.label(text="DccMax:")
        col.label(text="AccMove:")
        col.label(text="MaxAmp:")
        col.label(text="VelWin:")
        col.operator('ww.actuator_props_write',text ='Write')
        col = split.column() 
        col.prop(self,"ww_actuator_VelAccAmp_VelMaxMot_prop",text="")     
        col.prop(self,"ww_actuator_VelAccAmp_VelMax_prop",text="")
        col.prop(self,"ww_actuator_VelAccAmp_AccMax_prop",text="")
        col.prop(self,"ww_actuator_VelAccAmp_DccMax_prop",text="")
        col.prop(self,"ww_actuator_VelAccAmp_AccMove_prop",text="")
        col.prop(self,"ww_actuator_VelAccAmp_MaxAmp_prop",text="")
        col.prop(self,"ww_actuator_VelAccAmp_VelWin_prop",text="")
        col.operator('ww.actuator_props_cancel',text ='Cancel')
        
        colB1 = splitA.column(align=True)
        box = colB1.box()
        row = box.row(align=True)
        row.label(text="Guider")
        row = box.row(align=True)
        row.prop(self,"ww_actuator_Guider_Pos_prop",text="")  
        row.operator('ww.actuator_props_engage_guider',text ='Engage')
        row.prop(self,"ww_actuator_Guider_Vel_prop",text="")
        row = box.row(align=True)
        row.prop(self,"ww_actuator_Guider_State_prop",text="")  
        row.operator('ww.actuator_guider_reset',text ='Reset')
        row = box.row(align=True)
        row.prop(self,"ww_actuator_Guider_Ready_prop",text="Ready")  
        row.prop(self,"ww_actuator_Guider_Online_prop",text="online") 
        row = box.row(align=True)
        row.prop(self,"ww_actuator_VelAccAmp_VelMaxMot_prop",text="")
        box2 =box.box()
        row2 = box2.row(align=True)  
        row2.operator('ww.actuator_props_edit',text ='Edit')
        split = box2.split()
        col = split.column()
        col.label(text="Pitch:") 
        col.label(text="PosMax:") 
        col.label(text="PosMin:") 
        col = split.column()
        col.prop(self,"ww_actuator_Guider_Pitch_prop",text="") 
        col.prop(self,"ww_actuator_Guider_PosMax_prop",text="") 
        col.prop(self,"ww_actuator_Guider_PosMin_prop",text="") 
        col = split.column()
        col.operator('ww.actuator_props_write',text ='Write')
        col.label(text="Lag Error:") 
        col.operator('ww.actuator_props_cancel',text ='Cancel')
        
        colC = splitA.column(align=True)        
        box = colC.box() 
        row = box.row(align=True)
        row.label(text="Filter")
        row = box.row(align=True)
        row.operator('ww.actuator_props_edit',text ='Edit')
        split = box.split()
        col = split.column()
        col.label(text="Lag Error:") 
        col.label(text="Prop.:")
        col.label(text="Integral:")
        col.label(text="Derivate:")
        col.label(text="Int.Lim.:")
        col.label(text="Rampform:")
        col.label(text="")
        col.operator('ww.actuator_props_write',text ='Write')
        col = split.column()      
        col.prop(self,"ww_actuator_Filter_LagErr_prop",text="")
        col.prop(self,"ww_actuator_Filter_Prop_prop",text="")
        col.prop(self,"ww_actuator_Filter_Int_prop",text="")
        col.prop(self,"ww_actuator_Filter_Der_prop",text="")
        col.prop(self,"ww_actuator_Filter_IntLim_prop",text="")
        col.prop(self,"ww_actuator_Filter_Rampform_prop",text="")
        col.label(text="")
        col.operator('ww.actuator_props_cancel',text ='Cancel')
        
        colD = splitA.column(align=True)        
        box = colD.box() 
        row = box.row(align=True)
        row.label(text="Rope")
        row = box.row(align=True)
        row.operator('ww.actuator_props_edit',text ='Edit')
        split = box.split()
        col = split.column()
        col.label(text="SWLL:") 
        col.label(text="Diameter.:")
        col.label(text="Type:")
        col.label(text="Number:")
        col.label(text="Length:")
        col.label(text="")
        col.label(text="")
        col.operator('ww.actuator_props_write',text ='Write')
        col = split.column()      
        col.prop(self,"ww_actuator_Rope_SWLL_prop",text="")
        col.prop(self,"ww_actuator_Rope_Diameter_prop",text="")
        col.prop(self,"ww_actuator_Rope_Type_prop",text="")
        col.prop(self,"ww_actuator_Rope_Number_prop",text="")
        col.prop(self,"ww_actuator_Rope_Length_prop",text="")
        col.label(text="")
        col.label(text="")
        col.operator('ww.actuator_props_cancel',text ='Cancel')

        box = boxA.box()
        col = box.column(align = True)
        row1 = col.split(factor=0.91)    # Resync Btn
        row2 = row1.split(factor=0.90)   # Recover Btn
        row3 = row2.split(factor=0.99)   # Padding   
        row4 = row3.split(factor=0.85)   # PosDiff Value   
        row5 = row4.split(factor=0.92)    # PosDiff Label 
        row6 = row5.split(factor=0.67)    # CutTime
        row7 = row6.split(factor=0.99)   # Padding 
        row8 = row7.split(factor=0.7)   # CutVel Value   
        row9 = row8.split(factor=0.7)   # Cut Vel Label   
        row10= row9.split(factor=0.5)   # Cut Pos Value
        row11= row10.split(factor=1)      # Cut Pos Label
        row1.operator('ww.actuator_resync',text ='ReSync')
        row2.operator('ww.actuator_recover',text ='Recover')
        row3.label(text =' ')
        row4.prop(self,'ww_actuator_Recover_PosDiff_prop', text = '')
        row5.label(text =' PosDiff')
        row6.prop(self, 'ww_actuator_Recover_CutTime_prop', text = '')
        row7.label(text =' ')
        row8.prop(self, 'ww_actuator_Recover_CutVel_prop', text = '')
        row9.label(text =' CutVel')
        row10.prop(self, 'ww_actuator_Recover_CutPos_prop', text = '')
        row11.label(text =' CutPos')

        box = boxA.box()
        splitA = box.split()
        colA = splitA.column(align=True)            
        box = colA.box()
        split = box.split()
        col1 = split.column()
        col1.prop(self,'ww_actuator_EStop_Master_prop', text='Master')
        col1.prop(self,'ww_actuator_EStop_Slave_prop', text='Slave')
        col1.prop(self,'ww_actuator_EStop_Network_prop', text='Network')

        colB = splitA.column(align=True)
        box = colB.box() 
        row = box.row(align=True)
        split = box.split()
        col1A = split.column()
        col1A.operator('ww.actuator_guider_reset',text ='Reset')
        
        colB = splitA.column(align=True)
        box = colB.box() 
        row = box.row(align=True)
        split = box.split()
        col2 = split.column()
        col2.prop(self,'ww_actuator_EStop_EStop1_prop', text='E-Stop 1')
        col2.prop(self,'ww_actuator_EStop_EStop2_prop', text='E-Stop 2')
 
        colB = splitA.column(align=True)
        box = colB.box() 
        row = box.row(align=True)
        split = box.split()
        col3 = split.column()
        col3.prop(self,'ww_actuator_EStop_30kW_prop', text='30kW')
        col3.prop(self,'ww_actuator_EStop_05kW_prop', text='0.5kW')

        colB = splitA.column(align=True)
        box = colB.box() 
        row = box.row(align=True)
        split = box.split()
        col4 = split.column()
        col4.prop(self,'ww_actuator_EStop_Brk1_prop', text='Brk 1 OK')
        col4.prop(self,'ww_actuator_EStop_Brk2_prop', text='Brk 2 OK')
        col4.prop(self,'ww_actuator_EStop_Brk2Kb_prop', text='Brk 2 Kb')

        colB = splitA.column(align=True)
        box = colB.box() 
        row = box.row(align=True)
        split = box.split()
        col5 = split.column()
        col5.prop(self,'ww_actuator_EStop_SPS_prop', text='SPS OK')
        col5.prop(self,'ww_actuator_EStop_Red_prop', text='Red OK')
        col5.prop(self,'ww_actuator_EStop_Enc_prop', text='ENC OK')
    
        colB = splitA.column(align=True)
        box = colB.box() 
        row = box.row(align=True)
        split = box.split()
        col6 = split.column()
        col6.prop(self,'ww_actuator_EStop_PosWin_prop', text='Pos Win')
        col6.prop(self,'ww_actuator_EStop_VelWin_prop', text='Vel Win')
        col6.prop(self,'ww_actuator_EStop_Endlage_prop', text='Endlage')   
    
        colB = splitA.column(align=True)
        box = colB.box() 
        row = box.row(align=True)
        split = box.split()
        col7 = split.column()
        col7.prop(self,'ww_actuator_EStop_G1Com_prop', text='G1 COM')
        col7.prop(self,'ww_actuator_EStop_G1Out_prop', text='G1 OUT')
        col7.prop(self,'ww_actuator_EStop_G1FB_prop', text='G1 FB')    
    
        colB = splitA.column(align=True)
        box = colB.box() 
        row = box.row(align=True)
        split = box.split()
        col8 = split.column()
        col8.prop(self,'ww_actuator_EStop_G2Com_prop', text='G2 COM')
        col8.prop(self,'ww_actuator_EStop_G2Out_prop', text='G2 OUT')
        col8.prop(self,'ww_actuator_EStop_G2FB_prop', text='G2 FB')      
    
        colB = splitA.column(align=True)
        box = colB.box() 
        row = box.row(align=True)
        split = box.split()
        col9 = split.column()
        col9.prop(self,'ww_actuator_EStop_G3Com_prop', text='G3 COM')
        col9.prop(self,'ww_actuator_EStop_G3Out_prop', text='G3 OUT')
        col9.prop(self,'ww_actuator_EStop_G3FB_prop', text='G3 FB')     
   