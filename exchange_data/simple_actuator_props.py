import bpy

class simple_Actuator_props(bpy.types.PropertyGroup):
    bl_idname = "simpel_Actuator_props"
    def update_conf(self,context):
        self.update_confirm()

    simple_actuator_Amp_prop: bpy.props.FloatProperty(name = "Ampere",
                                                                description ="Amplifier Output",
                                                                default=999,
                                                                precision=0,
                                                                update = update_conf ) 
    simple_actuator_HardMax_prop: bpy.props.FloatProperty(name = "Hard Max",
                                                                description ="Maximum Position set in the PLC",
                                                                default=5.0,
                                                                precision=3,
                                                                update = update_conf)
    simple_actuator_ActPos_prop: bpy.props.FloatProperty(name = "Act Pos",
                                                                description ="Actual Position",
                                                                default=0.0,
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
       self.simple_actuator_confirm = False
       self.simple_actuator_confirmed = False

    def drawActuatorSetup(self, context, layout):

        boxA = layout.box()
        row = boxA.row()
        row.label(text='Simple Physical Actuator Setup')        
        
        box1 = boxA.split()
        row = box1.row()
        row.label(text = 'Max Pos')
        row.prop(self,'simple_actuator_HardMax_prop', text='')
        row.label(text = 'Min Pos')
        row.prop(self,'simple_actuator_HardMin_prop', text='')
        row.label(text = 'Max Vel')
        row.prop(self,'simple_actuator_VelMax_prop', text='')
        row.label(text = 'Max Acc')
        row.prop(self,'simple_actuator_AccMax_prop', text='')
        row.prop(self,'simple_actuator_confirm', text='')
        row.prop(self,'simple_actuator_confirmed', text='')
