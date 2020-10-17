import bpy

from .. exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset
from .. exchange_data.SFX_simple_actuator_Inset import SFX_simple_Actuator_Inset

class SFX_simpleCueNode(bpy.types.Node):
    ''' Takes Joystick Data and outputs selected Data'''
    bl_idname = 'SFX_simpleCueNode'
    bl_label = 'SimpleCue Node'
    bl_icon = 'ANCHOR_LEFT'
    bl_width_min = 580
    bl_width_max = 580

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    def update_value(self, context):
        self.update ()

    play_state_items = (('Play','Play','Play','PLAY',1),
                        ('Pause','Pause','Pause','PAUSE',2),
                        ('SpeedUp','Speed Up','Speeding Up to Play Speed','FF',3),
                        ('Slowing','Slowing','Slowing Down from Play Speed','REW',4),
                        ('Reverse','Reverse','Playing Reverse','PLAY_REVERSE',5),
                        ('GoTo1','Go To 1','Going To Start Position','FRAME_PREV',6))
        
    TickTime_prop : bpy.props.FloatProperty(default=0.0,
                                            update = update_value)
    max_Vel : bpy.props.FloatProperty(name='Max Vel',
                                      description='Max Vel of Cue',
                                      default = 0.0)
    max_Acc : bpy.props.FloatProperty(name='Max Acc',
                                      description='Max Acc of Cue',
                                      default = 0.0)
    duration : bpy.props.FloatProperty(name='Duration',
                                      description='Duration of Cue',
                                      default = 0.0)
    play_head_percent : bpy.props.FloatProperty(name='Play Head',
                                      description='Play Head',
                                      default = 60.0,
                                      soft_max = 100.0,
                                      soft_min = -100.0)
    play_head : bpy.props.FloatProperty(name='Play Head',
                                      description='Play Head',
                                      default = 0.0)
    play_state : bpy.props.EnumProperty(name='Play State',
                                       description = 'Play State of Cue',
                                       items = play_state_items,
                                       default = 'Pause')
    cue_min_pos: bpy.props.FloatProperty(name='Cue Min Pos',
                                      description='Cue Min Pos',
                                      default = 0.0) 
    cue_max_pos: bpy.props.FloatProperty(name='Cue Max Pos',
                                      description='Cue Max Pos',
                                      default = 0.0)
    cue_set_pos: bpy.props.FloatProperty(name='Cue Set Pos',
                                      description='Cue Set Pos',
                                      default = 0.0)
    cue_act_pos: bpy.props.FloatProperty(name='Cue Actual Pos',
                                      description='Cue Actual Pos',
                                      default = 0.0)
    cue_act_speed: bpy.props.FloatProperty(name='Cue Actual Speed',
                                      description='Cue Actual Speed',
                                      default = 0.0)
    cue_target_speed: bpy.props.FloatProperty(name='Cue Target Speed',
                                      description='Cue Target Speed',
                                      default = 0.0)                                                                           
    cue_diff_pos: bpy.props.FloatProperty(name='Cue Dif Pos',
                                      description='Difference Set Act Pos',
                                      default = 0.0)
    cue_diff_speed: bpy.props.FloatProperty(name='Cue Dif Speed',
                                      description='Difference Target Act Speed',
                                      default = 0.0) 
    confirm : bpy.props.BoolProperty(name = "Confirm Cue",
                                    description = "Confirm Cue",
                                    default = False)
    confirmed: bpy.props.BoolProperty(name = "Confiremd Cue",
                                    description = "The Confirmed Cue can be executed",
                                    default = False)
    ActConfirm: bpy.props.BoolProperty(name = "Actuator Confiremd",
                                    description = "The connected Actuator has confirmed properties",
                                    default = False)
    ActConfirmed: bpy.props.BoolProperty(name = "Actuator Confiremd",
                                    description = "The connected Actuator has confirmed properties",
                                    default = False)
    toTime : bpy.props.BoolProperty(name = "To Vel/Time",
                                    description = "To Vel over Time",
                                    default = False)                                            
    toTime_executed : bpy.props.BoolProperty(name = "To Vel/Time",
                                    description = "To Vel over Time",
                                    default = False) 

    operator_started_bit1 : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
                                    default = False)
    operator_running_modal: bpy.props.BoolProperty(name = "Operator Running Modal",
                                    description = "Operator Running Modal",
                                    default = False)

    operator_edit : bpy.props.BoolProperty(name = "Operator Edit",
                                    description = "Operator Edit",
                                    default = False)
    operator_editing : bpy.props.BoolProperty(name = "Operator Edit",
                                    description = "Operator Edit",
                                    default = False)

    expand_Actuator_props : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)
    length : bpy.props.FloatProperty(name = 'Length',
                                     description = 'Length of Actuator',
                                     default = 0)

    Actuator_props : bpy.props.PointerProperty(type = SFX_simple_Actuator_Inset)

    def init(self, context):
        self.outputs.new('SFX_Cue_Float', "Set Vel")
        self.outputs["Set Vel"].default_value_set = SFX_Joystick_Inset
        self.outputs["Set Vel"].ww_out_value = 0.0

        self.inputs.new('SFX_Cue_bool','Forward')
        self.inputs["Forward"].bool = False

        self.inputs.new('SFX_Cue_bool',name= 'Reverse')
        self.inputs["Reverse"].bool = False

        self.inputs.new('SFX_Cue_bool',name= 'Go To 1')
        self.inputs["Reverse"].bool = False

        self.spawnDataobject()

    def copy(self, node):
        print("copied node", node)
        
    def free(self):
        bpy.data.objects.remove(bpy.data.objects[self.name+'_Data'], do_unlink=True)
        bpy.data.actions.remove(bpy.data.actions[self.name+'_Cue'])
        self.operator_started_bit1 = False

    def draw_buttons(self, context, layout):
        split = layout.split(factor=0.65)
        col = split.column()
        box = col.box()
        col = box.column()
        row = col.row()
        row.prop(self,'play_state',text='')
        row.prop(self,'play_head',text='')
        row.prop(self,'play_head_percent',text='',slider = True)
        row.prop(self,'confirm',text='')
        row.prop(self,'confirmed',text='')
        row = box.row()
        col = row.column()
        col.label(text='Min Pos')
        col.prop(self,'cue_min_pos',text = '')
        col = row.column()
        col.label(text='Set Pos')
        col.prop(self,'cue_set_pos',text='')
        col.label(text='Act Speed')
        col.prop(self,'cue_act_speed',text ='')
        col = row.column()
        col.label(text='Act Pos')
        col.prop(self,'cue_act_pos',text='')
        col.label(text='Target Speed')
        col.prop(self,'cue_target_speed',text='')
        col = row.column()
        col.label(text='Delta')
        col.prop(self,'cue_diff_pos',text='')
        col.label(text='Delta')
        col.prop(self,'cue_diff_speed',text='')
        col = row.column()
        col.label(text='Max Pos')
        col.prop(self,'cue_max_pos',text='')

        col1 = split.column()
        box = col1.box()
        col = box.column()
        row4 = col.split(factor=0.75)         # Tick Time
        row5 = row4.split(factor=0.9)       # running modal
        row6 = row5.split(factor=0.9)       # started
        row7 = row6.split(factor=1)        # start
        row4.prop( self, 'TickTime_prop', text = '')
        row5.prop(self, 'operator_running_modal', text = '')
        row6.prop(self, 'operator_started_bit1', text = '')
        if not(self.operator_started_bit1):
            row7.operator('sfx.simplecueop',text ='Start')
        else:
            row7.operator('sfx.commstarteddiag',text ='Started')

        row = layout.row(align=True)
        row.prop(self, 'expand_Actuator_props')

        if self.expand_Actuator_props:
            row = layout.row(align=True)
            box = row.box()
            row = box.row()
            split2 = row.split(factor = 1)
            col2 = split2.column()
            split5 = row.split(factor = 1)
            col5 = split5.column()
            split6 = row.split(factor = 1)
            col6 = split6.column()
            split7 = row.split(factor = 1)
            col7 = split7.column()
            split8 = row.split(factor = 1)
            col8 = split8.column()
            split9 = row.split(factor = 1)
            col9 = split9.column()
            split10 = row.split(factor = 1)
            col10 = split10.column()
            split11 = row.split(factor = 1)
            col11 = split11.column()
            split12 = row.split(factor = 1)
            col12 = split12.column()
            split13 = row.split(factor = 1)
            col13 = split13.column()

            col2.prop(self,'toTime',text='')
            col5.prop(self,'toTime_executed',text='')
            col6.label(text='C Max Vel')
            col7.prop(self,'max_Vel',text='')
            col8.label(text='C Max Acc')
            col9.prop(self,'max_Acc',text='')
            col10.label(text='C Dur')
            col11.prop(self,'duration',text='')
            col12.prop(self,'confirm',text='')
            col13.prop(self,'confirmed',text='')

            row = box.row()
            self.Actuator_props.drawActuatorSetup(context, row)

    def update(self):
        try:
            out1 = self.outputs["Set Vel"]
            inp1 = self.inputs["Forward"]
            inp2 = self.inputs["Reverse"]
            inp3 = self.inputs['Go To 1']
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if inp1.is_linked:
                for i1 in inp1.links:
                    if i1.is_valid:
                        self.inputs["Forward"].bool=i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        pass
            if inp2.is_linked:
                for i2 in inp2.links:
                    if i2.is_valid:
                        self.inputs["Reverse"].bool=i2.from_socket.node.outputs[i2.from_socket.name].ww_out
                        pass
            if inp3.is_linked:
                for i3 in inp3.links:
                    if i3.is_valid:
                        self.inputs["Go To 1"].bool=i3.from_socket.node.outputs[i3.from_socket.name].ww_out
                        pass
            if out1.is_linked:
                 for o in out1.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].set_vel = self.outputs["Set Vel"].ww_out_value
                        self.Actuator_props.simple_actuator_HardMax_prop  = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
                        self.Actuator_props.simple_actuator_HardMin_prop  = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
                        self.Actuator_props.simple_actuator_VelMax_prop   = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop
                        self.Actuator_props.simple_actuator_AccMax_prop   = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop
                        self.Actuator_props.simple_actuator_confirm       = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_confirm
                        self.Actuator_props.simple_actuator_confirmed     = o.to_socket.node.Actuator_basic_props.Actuator_props.simple_actuator_confirmed
                        self.ActConfirm    = self.Actuator_props.simple_actuator_confirm
                        self.ActConfirmed  = self.Actuator_props.simple_actuator_confirmed
                        self.cue_min_pos   = self.Actuator_props.simple_actuator_HardMin_prop
                        self.cue_act_pos   = o.to_socket.node.Actuator_basic_props.ist_Pos
                        self.cue_act_speed = o.to_socket.node.Actuator_basic_props.ist_Vel
                        self.cue_diff_pos  = self.cue_act_pos - self.cue_set_pos
                        self.cue_max_pos   = self.Actuator_props.simple_actuator_HardMax_prop
                        self.length        = o.to_socket.node.Actuator_basic_props.DigTwin_basic_props.length
                        pass
                    else:
                        self.ActConfirm   = False
                        self.ActConfirmed = False
                        self.cue_min_pos  = 0.0
                        self.cue_act_pos  = 0.0
                        self.cue_diff_pos = 0.0
                        self.cue_max_pos  = 0.0
                        self.length       = 0.0

    def spawnDataobject(self):
        if 'ww SFX_Nodes' in bpy.context.scene.collection.children.keys():
            coll = bpy.data.collections.get("ww SFX_Nodes")
            self.Dataobject = bpy.data.objects.new( self.name+"_Data", None )
            self.Dataobject.empty_display_size = 2
            self.Dataobject.empty_display_type = 'CIRCLE'
            self.Dataobject.location = (0,0,0)
            coll.objects.link(self.Dataobject)