import bpy

from .. SFX_Action_Props import SFX_Action_Props

class SFX_Actuators_Expanded_Inset(bpy.types.PropertyGroup):
    '''Defines Physical Props of an Actuator'''
    bl_idname = "SFX_simple_Actuator_Inset"
    
    def update_HardMax(self,context):
        self.update_HardMax_do(context)

    def update_HardMin(self,context):
        self.update_HardMin_do(context)

    def update_VelMax(self,context):
        self.update_VelMax_do(context)
        
    def update_AccMax(self,context):
        self.update_AccMax_do(context)

    def update_index(self,context):
        self.update_index_do(context)

    simple_actuator_HardMax_prop: bpy.props.FloatProperty(name = "Hard Max",
                                                                description ="Maximum Position set in the PLC",
                                                                default=5.0,
                                                                precision=3,
                                                                update = update_HardMax)
    simple_actuator_HardMin_prop: bpy.props.FloatProperty(name = "Hard Min",
                                                                description ="Minimum Position set in the PLC",
                                                                default=0.0,
                                                                precision=3,
                                                                update = update_HardMin)
    simple_actuator_VelMax_prop: bpy.props.FloatProperty(name = "Vel Max",
                                                                description ="Maximum Velocity set in Program",
                                                                default=5.0,
                                                                precision=3,
                                                                update = update_VelMax)
    simple_actuator_AccMax_prop: bpy.props.FloatProperty(name = "Acc Max",
                                                                description ="Maximum Acceleration",
                                                                default=5.0,
                                                                precision=3,
                                                                update = update_AccMax)
    simple_actuator_Time_prop: bpy.props.FloatProperty(name = "Time",
                                                                description ="Time",
                                                                default=0.0,
                                                                precision=3)

    SFX_actions                 : bpy.props.CollectionProperty(type=SFX_Action_Props)
    SFX_actions_index           : bpy.props.IntProperty(name = "Index",
                                                                description ="Action Index",
                                                                default=0,
                                                                update = update_index)
    
    simple_actuator_confirm: bpy.props.BoolProperty(name = "Confirm Data",
                                    description = " Set to confirm Data",
                                    default = False)
    simple_actuator_confirmed: bpy.props.BoolProperty(name = "Confirmed Data",
                                    description = " Set if Data is confirmed",
                                    default = False)

    def drawActuatorSetup(self, context, layout):
        boxA = layout.box()
        row = boxA.row()
        row.label(text='Action Setup') 
        box1 = boxA.split(factor = 0.5)
        col = box1.column(align = True)
        #col = col.split(factor = 0.5)

        try:
            current_item = (self.SFX_actions[self.SFX_actions_index].name)
        except IndexError:
            current_item = ""
        rows = 3        
        col.template_list("SFX_UL_List", "", self, "SFX_actions", self, "SFX_actions_index", rows=rows)
        col = col.column(align=True)

        row = col.row()        
        col = boxA.column(align=True)
        rowsub = col.row(align=True)
        rowsub.operator("sfx.list_action", icon='ZOOM_IN', text="Load Action").action = 'ADD'
        rowsub.operator("sfx.list_action", icon='ZOOM_OUT', text="Un-Load Action").action = 'REMOVE'
        rowsub.operator("sfx.list_action", icon='FILE_TICK', text="Save Action").action = 'SAVE'
        row = col.row()
        col = row.column(align=True)
        col.operator("sfx.clear_list", icon="X")        


        col1= box1.column(align = True)
        col1 = col1.split(factor = 0.5)
        colA = col1.column()
        row = colA.row() 
        row.label(text = 'Min Pos')
        row.prop(self,'simple_actuator_HardMin_prop', text='')
        row = colA.row()
        row.label(text = 'Max Pos')
        row.prop(self,'simple_actuator_HardMax_prop', text='')

        col2 = col1.column()
        row = col2.row()
        row.label(text = 'Max Vel')
        row.prop(self,'simple_actuator_VelMax_prop', text='')
        row= col2.row()
        row.label(text = 'Max Acc')
        row.prop(self,'simple_actuator_AccMax_prop', text='')
        row1= col2.row()
        row1.label(text = 'Time')
        row1.prop(self,'simple_actuator_Time_prop', text='')
        row1.enabled = False
        row= col2.row()
        row = row.split(factor = 0.11)
        col= row.column()
        col.separator()
        col = row.column()
        col.prop(self,'simple_actuator_confirm', text='')
        col = row.column()
        col.prop(self,'simple_actuator_confirmed', text='')

    def update_index_do(self,context):
        bpy.ops.sfx.list_action('INVOKE_DEFAULT')
        return

    def update_HardMax_do(self,context):
        bpy.ops.sfx.maxpos_update('INVOKE_DEFAULT')
        return
    def update_HardMin_do(self,context):
        if self.simple_actuator_HardMin_prop > self.simple_actuator_HardMax_prop:
            self.simple_actuator_HardMin_prop = self.simple_actuator_HardMax_prop - 0.01
        bpy.ops.sfx.minpos_update('INVOKE_DEFAULT')
        return
    def update_VelMax_do(self,context):
        bpy.ops.sfx.maxvel_update('INVOKE_DEFAULT')
        return
    def update_AccMax_do(self,context):
        bpy.ops.sfx.maxacc_update('INVOKE_DEFAULT')
        return