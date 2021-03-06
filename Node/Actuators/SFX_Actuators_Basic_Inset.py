import bpy
import time

from . SFX_Actuators_Expanded_Inset import SFX_Actuators_Expanded_Inset
from . SFX_Digtwin_Basic_Inset import SFX_Digtwin_Basic_Inset 

class SFX_Actuators_Basic_Inset(bpy.types.PropertyGroup):
    ''' Inset with the Basic Properties of an Actuator''' 
    bl_idname = "SFX_actuator_basic_Inset"

    Actuator_props : bpy.props.PointerProperty(type = SFX_Actuators_Expanded_Inset)

    DigTwin_basic_props : bpy.props.PointerProperty(type = SFX_Digtwin_Basic_Inset)

    diff_Vel : bpy.props.FloatProperty(name = "Ist Pos",
                                    description = "Ist Position",
                                    precision = 3,
                                    default = 0.001)
    soll_Vel : bpy.props.FloatProperty(name = "Soll Vel",
                                    description = "Soll Velocity",
                                    precision = 3,
                                    default = 0.001)
    ist_Pos : bpy.props.FloatProperty(name = "Ist Pos",
                                    description = "Ist Pos",
                                    precision = 3,
                                    default = 0.001)
    ist_Force : bpy.props.FloatProperty(name = "Soll Force",
                                    description = "Soll Force",
                                    precision = 3,
                                    default = 0.001)
    ist_Vel : bpy.props.FloatProperty(name = "Ist Vel",
                                    description = "Ist Velocity",
                                    precision = 3,
                                    default = 0.001)
    enable_Actuator : bpy.props.BoolProperty(name = "Enable Actuator",
                                    description = " Enable Actuator",
                                    default = False)
    select_Actuator : bpy.props.BoolProperty(name = "Select Actuator",
                                    description = "Select Actuator",
                                    default = False)
    online_Actuator : bpy.props.BoolProperty(name = "Actuator Online",
                                    description = "Actuator Online",
                                    default = False)
    TickTime_A : bpy.props.StringProperty(name='TickTimeA',
                                     description ='TickTimeA',
                                     default ='1891011121314')    
    Status : bpy.props.StringProperty(name='TickTimeA',
                                     description ='TickTimeA',
                                     default ='OFF')
    expand_DigTwin_basic : bpy.props.BoolProperty(name = "Expand Digital Twin Basic",
                                    description = " Expand Digital Twin Basic",
                                    default = False)
    expand_Actuator_setup : bpy.props.BoolProperty(name = "Expand Action Setup",
                                    description = "Expand Action Setup",
                                    default = False)

    def draw_Actuator_basic_props(self, context, layout):
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
        col3.label(text='Ist Pos')
        col3.prop(self,'ist_Pos', text = '')        
        row4 = row3.split(factor=0.25)
        col4 = row4.column()
        col4.label(text='')
        col4.prop(self,"online_Actuator",text="Online")    
        row5 = row4.split(factor=0.3)
        col5 = row5.column()
        col5.label(text='') 
        col5.prop(self,'enable_Actuator',text="Enable")
        row6 = row5.split(factor=0.5)
        col6 = row6.column()
        col6.label(text='')        
        col6.prop(self,"select_Actuator",text="Select")
        row7 = row6.split(factor=1)
        col7 = row7.column()
        col7.label(text='Status')        
        col7.prop(self,"Status",text="")
    
        row3 = box.row(align=True)
        row3.prop(self, 'expand_DigTwin_basic')
        row3.prop(self, 'expand_Actuator_setup')

        if self.expand_DigTwin_basic:
            self.DigTwin_basic_props.draw_ww_DigTwin_basic_props(context, box) 

        if self.expand_Actuator_setup:
            self.Actuator_props.drawActuatorSetup(context, box)



    def unpackRecStringfromAxis(self,Data):
        Data = Data.split(';')
        self.TickTime_A                                         = Data[0]
        if ((self.Actuator_props.simple_actuator_HardMax_prop - float( Data[1]))>0.0001 or
            (self.Actuator_props.simple_actuator_HardMin_prop - float( Data[2]))>0.0001 or
            (self.Actuator_props.simple_actuator_VelMax_prop  - float( Data[3]))>0.0001 or
            (self.Actuator_props.simple_actuator_AccMax_prop  - float( Data[4]))>0.0001):
            self.Actuator_props.simple_actuator_confirm   = False
            self.Actuator_props.simple_actuator_confirmed = False

        self.ist_Vel                                             =float( Data[5])
        self.ist_Pos                                             =float( Data[6])
        #IstForce                                                =float( Data[7])
        #confirm                                                 =Data[8]
        if self.online_Actuator == True:
            if Data[9]=='False':
                self.Actuator_props.simple_actuator_confirmed = False
                pass
            else:
                self.Actuator_props.simple_actuator_confirmed = True
                pass
        else:
            self.Actuator_props.simple_actuator_confirmed = False
            pass

        #online                                                 =Data[10]
        #enabeled                                               =Data[11]
        self.Status                                             =Data[12]
        #Reset                                                  =Data[13]



    def packSendStringToAxis(self):
        SendData = self.TickTime_A
        SendData = (SendData+';'                                                     # 0
                    +str(self.Actuator_props.simple_actuator_HardMax_prop)+';'    # 1
                    +str(self.Actuator_props.simple_actuator_HardMin_prop)+';'    # 2
                    +str(self.Actuator_props.simple_actuator_VelMax_prop)+';'     # 3
                    +str(self.Actuator_props.simple_actuator_AccMax_prop)+';'     # 4            
                    +str(self.soll_Vel)+';'                                          # 5
                    +str('Soll Pos')+';   '                                          # 6
                    +str('Soll Force')+';'                                           # 7
                    +str(self.Actuator_props.simple_actuator_confirm)+';'         # 8
                    +str(self.Actuator_props.simple_actuator_confirmed)+';'       # 9
                    +str(self.enable_Actuator)+';'                                   # 10
                    +str(self.select_Actuator)+';'                                   # 11
                    +str(self.online_Actuator)+';'                                   # 12
                    +str('Status')+';'                                               # 13
                    +str('Reset'))                                                   # 14
        return SendData