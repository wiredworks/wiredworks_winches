import bpy

from . SFX_Actuators_ListProps import SFX_Actuators_ListProps 

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

    SFX_actions                 : bpy.props.CollectionProperty(type=SFX_Actuators_ListProps)
    SFX_actions_index           : bpy.props.IntProperty(name = "Index",
                                                                description ="Action Index",
                                                                default=0,
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
        row.label(text='Action Setup') 
        box1 = boxA.split(factor = 0.8)
        col = box1.column(align = True)
        try:
            current_item = (self.SFX_actions[self.SFX_actions_index].name)
        except IndexError:
            current_item = ""
        col = col.split(factor = 0.95)
        rows = 4        
        col.template_list("SFX_UL_List", "", self, "SFX_actions", self, "SFX_actions_index", rows=rows)
        #col.label(text = 'mist')
        col = col.column(align=True)
        col.operator("sfx.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("sfx.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = col.row()        
        col = boxA.column(align=True)
        rowsub = col.row(align=True)
        rowsub.operator("sfx.list_action", icon='ZOOM_IN', text="Add Action").action = 'ADD'
        rowsub.operator("sfx.list_action", icon='ZOOM_OUT', text="Remove Action").action = 'REMOVE'
        rowsub.operator("sfx.list_action", icon='FILE_TICK', text="Save Action").action = 'SAVE'
        row = col.row()
        col = row.column(align=True)
        col.operator("sfx.clear_list", icon="X")        
        # row = col.row(align = True)
        # row.label(text ="Active Action: {}".format(current_item))

        col1= box1.column()
        row = col1.row() 
        row.label(text = 'Min Pos')
        row.prop(self,'simple_actuator_HardMin_prop', text='')
        row = col1.row()
        row.label(text = 'Max Pos')
        row.prop(self,'simple_actuator_HardMax_prop', text='')
        row = col1.row()
        row.label(text = 'Max Vel')
        row.prop(self,'simple_actuator_VelMax_prop', text='')
        row= col1.row()
        row.label(text = 'Max Acc')
        row.prop(self,'simple_actuator_AccMax_prop', text='')
        row= col1.row()
        row = row.split(factor = 0.7)
        col= row.column()
        col.separator()
        col = row.column()
        col.prop(self,'simple_actuator_confirm', text='')
        col = row.column()
        col.prop(self,'simple_actuator_confirmed', text='')