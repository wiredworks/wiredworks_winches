import bpy

class SFX_Actuators_Expanded_Inset(bpy.types.PropertyGroup):
    '''Defines Physical Props of an Actuator'''
    bl_idname = "SFX_simple_Actuator_Inset"
    
    def update_conf(self,context):
        pass

    simple_actuator_HardMax_prop: bpy.props.FloatProperty(name = "Hard Max",
                                                                description ="Maximum Position set in the PLC",
                                                                default=5.0,
                                                                precision=3,
                                                                update = update_conf)
    simple_actuator_HardMin_prop: bpy.props.FloatProperty(name = "Hard Min",
                                                                description ="Minimum Position set in the PLC",
                                                                default=0.0,
                                                                precision=3,
                                                                update = update_conf)
    simple_actuator_VelMax_prop: bpy.props.FloatProperty(name = "Vel Max",
                                                                description ="Maximum Velocity set in Program",
                                                                default=5.0,
                                                                precision=3,
                                                                update = update_conf)
    simple_actuator_AccMax_prop: bpy.props.FloatProperty(name = "Acc Max",
                                                                description ="Maximum Acceleration",
                                                                default=5.0,
                                                                precision=3,
                                                                update = update_conf)
    
    simple_actuator_confirm: bpy.props.BoolProperty(name = "Confirm Data",
                                    description = " Set to confirm Data",
                                    default = False)
    simple_actuator_confirmed: bpy.props.BoolProperty(name = "Confirmed Data",
                                    description = " Set if Data is confirmed",
                                    default = False)

    def update_confirm(self):
       #self.simple_actuator_confirm = False 
       self.simple_actuator_confirmed = False
       pass

    def drawActuatorSetup(self, context, layout):

        boxA = layout.box()
        row = boxA.row()
        row.label(text='Simple Physical Actuator Setup')        
        
        box1 = boxA.split()
        row = box1.row()
        row.label(text = 'Min Pos')
        row.prop(self,'simple_actuator_HardMin_prop', text='')
        row.label(text = 'Max Pos')
        row.prop(self,'simple_actuator_HardMax_prop', text='')
        row.label(text = 'Max Vel')
        row.prop(self,'simple_actuator_VelMax_prop', text='')
        row.label(text = 'Max Acc')
        row.prop(self,'simple_actuator_AccMax_prop', text='')
        row.prop(self,'simple_actuator_confirm', text='')
        row.prop(self,'simple_actuator_confirmed', text='')
